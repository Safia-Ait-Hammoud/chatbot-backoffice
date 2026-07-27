from functools import lru_cache

from fastapi import Depends

from app.clients.embedding_client import EmbeddingClient
from app.clients.qdrant_client import QdrantWrapper
from app.clients.s3_client import S3Client
from app.core.config import get_settings
from app.services.faq_indexing_service import FAQIndexingService
from app.services.faq_log_service import FAQLogService
from app.services.faq_management_service import FAQManagementService


@lru_cache
def get_s3_client() -> S3Client:
    return S3Client(get_settings())


@lru_cache
def get_qdrant_client() -> QdrantWrapper:
    return QdrantWrapper(get_settings())


@lru_cache
def get_embedding_client() -> EmbeddingClient:
    return EmbeddingClient(get_settings())


def get_faq_log_service(
    s3_client: S3Client = Depends(get_s3_client),
) -> FAQLogService:
    return FAQLogService(s3_client)


def get_faq_indexing_service(
    embedding_client: EmbeddingClient = Depends(get_embedding_client),
    qdrant_client: QdrantWrapper = Depends(get_qdrant_client),
) -> FAQIndexingService:
    return FAQIndexingService(embedding_client, qdrant_client)


def get_faq_management_service(
    s3_client: S3Client = Depends(get_s3_client),
    log_service: FAQLogService = Depends(get_faq_log_service),
    indexing_service: FAQIndexingService = Depends(get_faq_indexing_service),
) -> FAQManagementService:
    return FAQManagementService(s3_client, log_service, indexing_service)