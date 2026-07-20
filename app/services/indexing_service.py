import uuid
from repositories.document_repository import DocumentRepository
from services.extractor_service import Extractor
from services.textCleaner_service import TextCleaner
from services.s3_service import S3Service
from services.chunking_service import ChunkingService
from langchain_text_splitters import MarkdownHeaderTextSplitter


class IndexingService:

    def __init__(self):
        self.document_repository = DocumentRepository()
        self.s3_service = S3Service()
        self.extractor = Extractor()
        self.text_cleaner = TextCleaner()
        self.chunking_service = ChunkingService()


    async def prepare_document(
        self,
        document_id: str,
            ) -> dict:
        document = await self.document_repository.get_by_id(document_id)
        if document is None:
            raise Exception("Document introuvable.")

        file_bytes = await self.s3_service.download_file(document["s3_key"])
        extracted_text = self.extractor.extract(file_bytes)
        cleaned_text = self.text_cleaner.clean(extracted_text)
        chunks = await self.chunking_service.parent_child_chunk(document, cleaned_text)

        return chunks


        
