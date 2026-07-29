from bson import ObjectId

from app.clients.mongo_client import MongoClient
from app.schemas.docs.document_model import DocumentModel


class DocumentRepository:
    COLLECTION_NAME = "documents"

    def __init__(self, mongo_client: MongoClient):
        self._collection = mongo_client.get_collection(self.COLLECTION_NAME)

    async def create(self, document: DocumentModel) -> str:
        result = await self._collection.insert_one(document.model_dump())
        return str(result.inserted_id)

    async def update(self, document_id: str, updated_doc: DocumentModel) -> bool:
        result = await self._collection.update_one(
            {"_id": ObjectId(document_id)},
            {"$set": updated_doc.model_dump(exclude={"id"})},
        )
        return result.modified_count > 0

    async def get_by_id(self, document_id: str) -> dict | None:
        document = await self._collection.find_one({"_id": ObjectId(document_id)})
        if not document:
            return None
        document["id"] = str(document.pop("_id"))
        return document

    async def list_by_project(self, project_id: str) -> list[dict]:
        documents = []
        async for document in self._collection.find({"project_id": project_id}):
            document["id"] = str(document.pop("_id"))
            documents.append(document)
        return documents

    async def delete_by_id(self, document_id: str) -> bool:
        result = await self._collection.delete_one({"_id": ObjectId(document_id)})
        return result.deleted_count > 0