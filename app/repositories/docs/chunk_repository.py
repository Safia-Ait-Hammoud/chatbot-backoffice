from fastapi import HTTPException
from qdrant_client.models import (
    PointStruct,
    VectorParams,
    Distance,
    Filter,
    FieldCondition,
    MatchValue,
)

from app.clients.mongo_client import MongoClient
from app.clients.qdrant_client import QdrantWrapper
from app.repositories.docs.project_repository import ProjectRepository
from app.schemas.docs.chunk_model import ParentModel, ChildModel


class ChunkRepository:
    COLLECTION_NAME = "parents"

    def __init__(
        self,
        mongo_client: MongoClient,
        qdrant_client: QdrantWrapper,
        project_repository: ProjectRepository,
    ):
        self._collection = mongo_client.get_collection(self.COLLECTION_NAME)
        self._qdrant = qdrant_client
        self._projects = project_repository

    # --- Mongo : parents ---

    async def create_parent(self, parent: ParentModel) -> str:
        document = parent.model_dump(by_alias=True)
        result = await self._collection.insert_one(document)
        return str(result.inserted_id)

    async def create_many_parents(self, parents: list[ParentModel]) -> list[str]:
        if not parents:
            return []
        documents = [parent.model_dump(by_alias=True) for parent in parents]
        result = await self._collection.insert_many(documents)
        return [str(inserted_id) for inserted_id in result.inserted_ids]

    async def get_parent_by_id(self, parent_id: str) -> dict | None:
        parent = await self._collection.find_one({"_id": parent_id})
        if not parent:
            return None
        parent["id"] = str(parent.pop("_id"))
        return parent

    async def get_parents_by_document_id(self, document_id: str) -> list[dict]:
        parents = []
        async for parent in self._collection.find({"document_id": document_id}):
            parent["id"] = str(parent.pop("_id"))
            parents.append(parent)
        return parents

    # --- Qdrant : children ---

    async def create_many_children(self, project_id: str, children: list[ChildModel]) -> dict:
        if not children:
            return {"collection": None, "inserted_count": 0}

        project = await self._projects.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Projet introuvable")

        collection_name = project["name"]

        points = [
            PointStruct(
                id=child.child_id,
                vector=child.vector,
                payload=child.payload.model_dump(),
            )
            for child in children
        ]

        self._qdrant.upsert_points(collection_name, points)
        return {"collection": collection_name, "inserted_count": len(points)}

    async def delete_doc_chunks(self, project_id: str, document_id: str) -> None:
        project = await self._projects.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Projet introuvable")

        await self._collection.delete_many({"document_id": document_id})

        self._qdrant.delete_by_filter(
            collection_name=project["name"],
            filter_=Filter(
                must=[FieldCondition(key="document_id", match=MatchValue(value=document_id))]
            ),
        )