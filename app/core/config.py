from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    bucket_name: str
    aws_region: str = "eu-west-3"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None

    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: Optional[str] = None
    
    openai_api_key: str
    openai_embedding_model: str = "text-embedding-3-large"

    
    mongodb_uri: str
    mongodb_db_name: str

    openai_dimensions: int = 3072
    
    qdrant_vector_size: int = 3072

    bm25_model :str = "Qdrant/bm25"



@lru_cache
def get_settings() -> Settings:
    return Settings()

