from bson import ObjectId

from core.mongodb import mongo_db
from models.document_model import DocumentModel

collection = mongo_db["documents"]


class DocumentRepository:

    async def create(self, document: DocumentModel) -> str:
        result = await collection.insert_one(document.model_dump())
        return str(result.inserted_id)

    async def get_by_id(self, document_id: str) -> dict | None:
        document = await collection.find_one({"_id": ObjectId(document_id)})

        if not document:
            return None

        document["id"] = str(document.pop("_id"))
        return document

    async def list_by_project(self, project_id: str) -> list[dict]:
        documents = []

        cursor = collection.find({"project_id": project_id})

        async for document in cursor:
            document["id"] = str(document.pop("_id"))
            documents.append(document)

        return documents

    async def delete_by_id(self, document_id: str) -> bool:
        result = await collection.delete_one({"_id": ObjectId(document_id)})
        return result.deleted_count > 0


        
        