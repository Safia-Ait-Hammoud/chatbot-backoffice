from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)

from app.core.config import Settings


class MongoClient:
    def __init__(self, settings: Settings):
        self._client = AsyncIOMotorClient(settings.mongodb_uri)
        self._db: AsyncIOMotorDatabase = self._client[settings.mongodb_db_name]

    def get_collection(self, name: str) -> AsyncIOMotorCollection:
        return self._db[name]