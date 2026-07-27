
from models.chunk_model import ParentModel ,ChildModel
from core.settings import settings
from core.settings import mongo_db
from qdrant_client.models import PointStruct, VectorParams, Distance
from repositories.project_repository import ProjectRepository
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
)

class ChunkRepository:
    def __init__(self):
        #mongo db
        self.collection = mongo_db["parents"]
        #qdrant
        self.client = settings.QDRANT_CLIENT
        self.vector_size = settings.DIMENSIONS

# stocker les parents sur mongo db
    
    async def create_parent(self, parent: ParentModel) -> str:
        document = parent.model_dump(by_alias=True)  # respecte l'alias "_id"
        result = await self.collection.insert_one(document)
        return str(result.inserted_id)

    async def create_manyParents(self, parents: list[ParentModel]) -> list[str]:
        if not parents:
            return []

        documents = [parent.model_dump(by_alias=True) for parent in parents]
        result = await self.collection.insert_many(documents)
        return [str(inserted_id) for inserted_id in result.inserted_ids]


    async def get_parent_by_id(self, parent_id: str) -> dict | None:
        parent = await self.collection.find_one({"_id": parent_id})

        if not parent:
            return None

        parent["id"] = str(parent.pop("_id"))
        return parent

    async def get_parents_by_document_id(self, document_id: str) -> list[dict]:
        parents_cursor = self.collection.find({"document_id": document_id})
        parents = []
        async for parent in parents_cursor:
            parent["id"] = str(parent.pop("_id"))
            parents.append(parent)
        return parents

# qdrant : stocker les enfants sur qdrant

    async def ensure_collection(self, collection_name: str) -> None:
        #Crée la collection si elle n'existe pas déjà.
        exists = self.client.collection_exists(collection_name)
        if not exists:
            await self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE,  # ou EUCLID / DOT selon ton besoin
                ),
            )

    
    async def create_many_children(self, project_id: str, children: list[ChildModel]) -> dict:
        if not children:
            return
        project = await ProjectRepository().get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Projet introuvable")
        collection_name = f"{project['name']}"
        await self.ensure_collection(collection_name)

        points = [
            PointStruct(
                id=child.child_id,
                vector=child.vector,
                payload=child.payload.model_dump(),
            )
            for child in children
        ]

        result =  self.client.upsert(collection_name=collection_name, points=points)
        return {
            "collection": collection_name,
            "inserted_count": len(points),
            }






    async def delete_doc_chunks(
        self,
        project_id: str,
        document_id: str,
        ) -> None:

        project = await ProjectRepository().get_by_id(project_id)

        await self.collection.delete_many(
            {"document_id": document_id}
        )

        self.client.delete(
            collection_name=project["name"],
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id),
                    )
                ]
            ),
        )