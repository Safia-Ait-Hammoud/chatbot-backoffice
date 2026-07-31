from app.clients.mongo_client import MongoClient
from app.schemas.faq.upload import FAQFileMetadata


class FAQFileRepository:
    COLLECTION_NAME = "faq_files"

    def __init__(self, mongo_client: MongoClient):
        self._collection = mongo_client.get_collection(self.COLLECTION_NAME)

    async def insert(self, metadata: FAQFileMetadata) -> None:
        """Un seul document par produit — on suppose ici qu'il n'existe pas encore."""
        data = metadata.model_dump(exclude={"id"})
        await self._collection.insert_one(data)

    async def get_by_product(self, product_id: str) -> dict | None:
        doc = await self._collection.find_one({"product_id": product_id})
        if not doc:
            return None
        doc["id"] = str(doc.pop("_id"))
        return doc

    async def delete_by_product(self, product_id: str) -> bool:
        result = await self._collection.delete_one({"product_id": product_id})
        return result.deleted_count > 0