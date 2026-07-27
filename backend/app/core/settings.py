from pathlib import Path
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from qdrant_client import QdrantClient

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


class Settings:
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
    DIMENSIONS = int(os.getenv("DIMENSIONS", "3072"))

    # AWS S3
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    AWS_BUCKET_NAME = os.getenv("BUCKET_NAME")

    # Qdrant
    QDRANT_URL = os.getenv("QDRANT_URL")
    #cient qdrant :
    QDRANT_CLIENT = QdrantClient(url=QDRANT_URL)

    # MongoDB
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME = os.getenv("MONGO_DB", "backoffice")


settings = Settings()

# Client Mongo
mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
mongo_db = mongo_client[settings.MONGO_DB_NAME]


