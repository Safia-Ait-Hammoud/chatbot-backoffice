from fastapi import HTTPException, UploadFile

from services.s3_service import S3Service
from models.document_model import DocumentModel
from repositories.document_repository import DocumentRepository
from repositories.project_repository import ProjectRepository


class DocumentService:

    def __init__(self):
        self.s3_service = S3Service()
        self.document_repository = DocumentRepository()
        self.project_repository = ProjectRepository()

    async def add_file(self, file: UploadFile, project_id: str) -> dict:

        project = await self.project_repository.get_by_id(project_id)

        if not project:
            raise HTTPException(
                status_code=404,
                detail="Projet introuvable"
            )

        result = await self.s3_service.upload_file(file, project["name"])

        document = DocumentModel(
            project_id=project_id,
            filename=result["filename"],
            s3_key=result["s3_key"],
            url=result["url"]
        )

        try:
            document_id = await self.document_repository.create(document)
        except Exception as e:
            await self.s3_service.delete_file(result["s3_key"])
            raise HTTPException(
                status_code=500,
                detail=f"Erreur MongoDB : {str(e)}"
            )

        return {
            "id": document_id,
            "filename": document.filename,
            "project_id": project_id,
            "s3_key": document.s3_key,
            "url": document.url
        }

    async def list_documents(self, project_id: str):
        return await self.document_repository.list_by_project(project_id)

    async def delete_document(self, document_id: str):

        document = await self.document_repository.get_by_id(document_id)

        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document introuvable"
            )

        await self.s3_service.delete_file(document["s3_key"])

        await self.document_repository.delete_by_id(document_id)

        return {
            "id": document_id,
            "deleted": True,
        }

    async def download_document(self, document_id: str) -> bytes:

        document = await self.document_repository.get_by_id(document_id)

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document introuvable"
            )

        return await self.s3_service.download_file(document["s3_key"])