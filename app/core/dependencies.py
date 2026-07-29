from functools import lru_cache

from fastapi import Depends

from app.clients.embedding_client import EmbeddingClient
from app.clients.qdrant_client import QdrantWrapper
from app.clients.s3_client import S3Client
from app.core.config import get_settings
from app.services.faq.faq_indexing_service import FAQIndexingService
from app.services.faq.faq_log_service import FAQLogService
from app.services.faq.faq_management_service import FAQManagementService

from app.services.docs.document_service import DocumentService
from app.services.docs.extractor_service import Extractor
from app.services.docs.textCleaner_service import TextCleaner
from app.services.docs.chunking_service import ChunkingService
from app.services.docs.ChunkStorage_service import ChunkStorageService
from app.services.docs.project_service import ProjectService
from app.services.docs.document_indexing_service import DocumentIndexingService


from app.clients.mongo_client import MongoClient
from app.repositories.docs.project_repository import ProjectRepository
from app.repositories.docs.document_repository import DocumentRepository
from app.repositories.docs.chunk_repository import ChunkRepository
from app.repositories.docs.chunk_repository import ChunkRepository


@lru_cache
def get_s3_client() -> S3Client:
    return S3Client(get_settings())


@lru_cache
def get_qdrant_client() -> QdrantWrapper:
    return QdrantWrapper(get_settings())


@lru_cache
def get_embedding_client() -> EmbeddingClient:
    return EmbeddingClient(get_settings())

@lru_cache
def get_mongo_client() -> MongoClient:
    return MongoClient(get_settings())


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



def get_project_repository(
    mongo_client: MongoClient = Depends(get_mongo_client),
) -> ProjectRepository:
    return ProjectRepository(mongo_client)


def get_document_repository(
    mongo_client: MongoClient = Depends(get_mongo_client),
) -> DocumentRepository:
    return DocumentRepository(mongo_client)


def get_chunk_repository(
    mongo_client: MongoClient = Depends(get_mongo_client),
    qdrant_client: QdrantWrapper = Depends(get_qdrant_client),
    project_repository: ProjectRepository = Depends(get_project_repository),
) -> ChunkRepository:
    return ChunkRepository(mongo_client, qdrant_client, project_repository)

def get_document_service(
    s3_client: S3Client = Depends(get_s3_client),
    document_repository: DocumentRepository = Depends(get_document_repository),
    project_repository: ProjectRepository = Depends(get_project_repository),
) -> DocumentService:
    return DocumentService(s3_client, document_repository, project_repository)


def get_extractor() -> Extractor:
    return Extractor()


def get_text_cleaner() -> TextCleaner:
    return TextCleaner()


def get_chunking_service() -> ChunkingService:
    return ChunkingService()


def get_chunk_storage_service(
    chunk_repository: ChunkRepository = Depends(get_chunk_repository),
    embedding_client: EmbeddingClient = Depends(get_embedding_client),
) -> ChunkStorageService:
    return ChunkStorageService(chunk_repository, embedding_client)


def get_project_service(
    project_repository: ProjectRepository = Depends(get_project_repository),
) -> ProjectService:
    return ProjectService(project_repository)


def get_document_indexing_service(
    document_service: DocumentService = Depends(get_document_service),
    s3_client: S3Client = Depends(get_s3_client),
    extractor: Extractor = Depends(get_extractor),
    text_cleaner: TextCleaner = Depends(get_text_cleaner),
    chunking_service: ChunkingService = Depends(get_chunking_service),
    chunk_storage_service: ChunkStorageService = Depends(get_chunk_storage_service),
) -> DocumentIndexingService:
    return DocumentIndexingService(
        document_service=document_service,
        s3_client=s3_client,
        extractor=extractor,
        text_cleaner=text_cleaner,
        chunking_service=chunking_service,
        chunk_storage_service=chunk_storage_service,
    )


