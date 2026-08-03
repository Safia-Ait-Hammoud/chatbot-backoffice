from fastapi import HTTPException

from app.clients.s3_client import S3Client
from app.repositories.docs.document_repository import DocumentRepository
from app.services.docs.extractor_service import Extractor
from app.services.docs.textCleaner_service import TextCleaner
from app.services.docs.chunking_service import ChunkingService
from app.services.docs.ChunkStorage_service import ChunkStorageService


class DocumentIndexingService:
    def __init__(
        self,
        document_repository : DocumentRepository,
        s3_client: S3Client,
        extractor: Extractor,
        text_cleaner: TextCleaner,
        chunking_service: ChunkingService,
        chunk_storage_service: ChunkStorageService,
    ):
        self._documents = document_repository
        self._s3 = s3_client
        self._extractor = extractor
        self._text_cleaner = text_cleaner
        self._chunking = chunking_service
        self._chunk_storage = chunk_storage_service

    async def index_document(self, document_id: str):
        document = await self._documents.get_by_id(document_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Document introuvable")

        file_bytes = await self._s3.download_file(document["s3_key"])
        extracted_text = self._extractor.extract(file_bytes)
        cleaned_text = self._text_cleaner.clean(extracted_text)
        chunks = await self._chunking.parent_child_chunk(cleaned_text)

        return await self._chunk_storage.chunks_storage(
            chunks,
            document["project_id"],
            document_id
        )

    async def reindex_document(self, document_id: str):

        document = await self._documents.get_by_id(document_id)
        await self._chunk_storage.delete_doc_chunks(
            document["project_id"],
            document_id
        )

        result = await self.index_document(document_id)

        return result