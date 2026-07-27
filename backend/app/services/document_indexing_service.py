from services.document_service import DocumentService
from services.s3_service import S3Service
from services.extractor_service import Extractor
from services.textCleaner_service import TextCleaner
from services.chunking_service import ChunkingService
from services.ChunkStorage_service import ChunkStorageService


class DocumentIndexingService:

    def __init__(
        self,
        document_service: DocumentService,
        s3_service: S3Service,
        extractor: Extractor,
        text_cleaner: TextCleaner,
        chunking_service: ChunkingService,
        chunk_storage_service: ChunkStorageService,
    ):
        self.document_service = document_service
        self.s3_service = s3_service
        self.extractor = extractor
        self.text_cleaner = text_cleaner
        self.chunking_service = chunking_service
        self.chunk_storage_service = chunk_storage_service

    async def index_document(self, document_id: str):
        document = await self.document_service.get_document_by_id(document_id)

        if document is None:
            raise Exception("Document introuvable.")

        file_bytes = await self.s3_service.download_file(document.s3_key)

        extracted_text = self.extractor.extract(file_bytes)

        cleaned_text = self.text_cleaner.clean(extracted_text)

        chunks = await self.chunking_service.parent_child_chunk(cleaned_text)
        
        result = await self.chunk_storage_service.chunks_storage(
            chunks,
            document.project_id,
            document_id,
        )

        return result



    async def reindex_document(self , document_id: str):
        document= await self.document_service.get_document_by_id(document_id)
        await self.chunk_storage_service.delete_doc_chunks(
            document.project_id,
            document.id)

        result =await self.index_document(document_id)
        return result
