from fastapi import Depends
from services.document_service import DocumentService
from services.s3_service import S3Service
from services.extractor_service import Extractor
from services.textCleaner_service import TextCleaner
from services.chunking_service import ChunkingService
from services.ChunkStorage_service import ChunkStorageService
from services.embedding_service import EmbeddingService
from services.project_service import ProjectService
from services.document_indexing_service import DocumentIndexingService




def get_document_service():
    return DocumentService()


def get_s3_service():
    return S3Service()


def get_extractor():
    return Extractor()


def get_text_cleaner():
    return TextCleaner()


def get_chunking_service():
    return ChunkingService()


def get_chunk_storage_service():
    return ChunkStorageService()


def get_embedding_service():
    return EmbeddingService()


def get_project_service():
    return ProjectService()

def get_document_indexing_service():
    return DocumentIndexingService(
        document_service=get_document_service(),
        s3_service=get_s3_service(),
        extractor=get_extractor(),
        text_cleaner=get_text_cleaner(),
        chunking_service=get_chunking_service(),
        chunk_storage_service=get_chunk_storage_service(),
    )