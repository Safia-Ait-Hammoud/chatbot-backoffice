from fastapi import HTTPException

from app.clients.embedding_client import EmbeddingClient
from app.repositories.docs.chunk_repository import ChunkRepository
from app.schemas.docs.chunk_model import ChildModel, ChildPayload, ParentModel, ParentChildMetadata ,ChildVectors ,SparseVectorModel
from app.schemas.docs.chunks_storage_response import ChunksStorageResponse


class ChunkStorageService:
    """
    Service orchestrant la sauvegarde des chunks (parents + enfants) :
    - persistance des parents en base documentaire (MongoDB)
    - génération des embeddings puis persistance des enfants en base vectorielle (Qdrant)
    """

    def __init__(self, chunk_repository: ChunkRepository, embedding_client: EmbeddingClient):
        self._chunks = chunk_repository
        self._embedding = embedding_client

    async def chunks_storage(
        self,
        chunks: dict,
        project_id: str,
        document_id: str,
    ) -> ChunksStorageResponse:

        # parents
        parents_to_create = [
            ParentModel(
                id=parent["parent_id"],
                parent_index=parent["parent_index"],
                content=parent["content"],
                metadata=ParentChildMetadata(
                    H1=parent["metadata"].get("H1"),
                    H2=parent["metadata"].get("H2"),
                ),
                project_id=project_id,
                document_id=document_id,
            )
            for parent in chunks["parents"]
        ]

        result_parents = await self._chunks.create_many_parents(parents_to_create)
        if not result_parents:
            raise HTTPException(status_code=500, detail="Erreur lors de la création des parents")

        # children



        flat_children = [
            (child, parent["parent_id"], parent["parent_index"])
            for parent in chunks["parents"]
            for child in parent["children"]
        ]

        contents = [child["content"] for child, _, _ in flat_children]

        embeddings = await self._embedding.generate_many(contents)
        sparse_embeddings = await self._embedding.generate_sparse_embeddings(contents)

        children_to_create = [
            ChildModel(
                child_id=child["child_id"],
                vectors=ChildVectors(
                    dense=embedding,
                    bm25=SparseVectorModel(
                        indices=sparse_vec["indices"],
                        values=sparse_vec["values"],
                    ),
                ),
                payload=ChildPayload(
                    project_id=project_id,
                    document_id=document_id,
                    parent_id=parent_id,
                    parent_index=parent_index,
                    child_index=child["metadata"]["chunk_index"],
                    content=child["content"],
                ),
            )
            for (child, parent_id, parent_index), embedding, sparse_vec in zip(
                flat_children, embeddings, sparse_embeddings
            )
        ]

        result = await self._chunks.create_many_children(project_id, children_to_create)
        return ChunksStorageResponse.model_validate(result)


    async def delete_doc_chunks(self, project_id: str, document_id: str) -> bool:
        return await self._chunks.delete_doc_chunks(project_id, document_id)