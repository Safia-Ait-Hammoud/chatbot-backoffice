from fastapi import HTTPException, UploadFile

from app.clients.s3_client import S3Client
from app.repositories.docs.chunk_repository import ChunkRepository
from app.repositories.docs.document_repository import DocumentRepository
from app.repositories.docs.project_repository import ProjectRepository
from app.schemas.docs.document_model import DocumentModel
from app.schemas.docs.document_model import DocumentResponse


class DocumentService:

    def __init__(
        self,
        s3_client: S3Client,
        document_repository: DocumentRepository,
        project_repository: ProjectRepository,
        chunks_repository: ChunkRepository
    ):
        self._s3 = s3_client
        self._documents = document_repository
        self._projects = project_repository
        self._chunks = chunks_repository

    async def add_file(self, file: UploadFile, project_id: str, filename: str) -> DocumentResponse:
        """Upload un nouveau fichier sur S3 et enregistre ses métadonnées en base."""
        project = await self._projects.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Projet introuvable")

        result = await self._s3.upload_file(file, project["name"])

        document = DocumentModel(
            project_id=project_id,
            filename=filename if filename else result["filename"],
            s3_key=result["s3_key"],
            url=result["url"],
        )

        try:
            document_id = await self._documents.create(document)
        except Exception as exc:
            await self._s3.delete_file(result["s3_key"])
            raise HTTPException(status_code=500, detail=f"Erreur MongoDB : {exc}") from exc

        return DocumentResponse(
            id=document_id,
            project_id=project_id,
            filename=document.filename,
            s3_key=document.s3_key,
            url=document.url,
        )

    async def update_doc(
        self, document_id: str, file: UploadFile = None, filename: str = None
    ) -> DocumentResponse:
        """Met à jour un document existant : le nom, le fichier, ou les deux."""
        if not file and not filename:
            raise HTTPException(status_code=400, detail="Aucune modification fournie (file ou filename requis)")

        old_doc = await self._documents.get_by_id(document_id)
        if not old_doc:
            raise HTTPException(status_code=404, detail="Document introuvable")

        project = await self._projects.get_by_id(old_doc["project_id"])
        if not project:
            raise HTTPException(status_code=404, detail="Projet introuvable")

        new_filename = old_doc["filename"]
        new_s3_key = old_doc["s3_key"]
        new_url = old_doc["url"]

        if file:
            result = await self._s3.upload_file(file, project["name"])
            new_s3_key = result["s3_key"]
            new_url = result["url"]
            new_filename = filename if filename else result["filename"]
        elif filename:
            new_filename = filename

        new_doc = DocumentModel(
            project_id=old_doc["project_id"],
            filename=new_filename,
            s3_key=new_s3_key,
            url=new_url,
        )

        try:
            updated = await self._documents.update(document_id, new_doc)
            if not updated:
                raise HTTPException(status_code=404, detail="Document introuvable ou non modifié")
        except HTTPException:
            if file:
                await self._s3.delete_file(new_s3_key)
                await self._chunks.delete_by_document_id(project["id"] , document_id)
            raise
        except Exception as exc:
            if file:
                await self._s3.delete_file(new_s3_key)
            raise HTTPException(status_code=500, detail=f"Erreur MongoDB : {exc}") from exc

        if file:
            try:
                await self._s3.delete_file(old_doc["s3_key"])
            except Exception as exc:
                raise HTTPException(
                    status_code=500, detail=f"Erreur lors de la suppression du fichier S3 : {exc}"
                ) from exc

        return DocumentResponse(
            id=old_doc["id"],
            project_id=new_doc.project_id,
            filename=new_doc.filename,
            s3_key=new_doc.s3_key,
            url=new_doc.url,
        )

    async def list_documents(self, project_id: str) -> list[DocumentResponse]:
        docs = await self._documents.list_by_project(project_id)
        return [DocumentResponse.model_validate(doc) for doc in docs]

    async def get_document_by_id(self, document_id: str) -> DocumentResponse:
        doc = await self._documents.get_by_id(document_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document introuvable")
        return DocumentResponse.model_validate(doc)

    async def get_documents_by_project_id(self, project_id: str) -> list[DocumentResponse]:
        docs = await self._documents.list_by_project(project_id)
        return [DocumentResponse.model_validate(doc) for doc in docs]

    async def delete_document(self, document_id: str) -> dict:
        """Supprime un document : son fichier sur S3 puis ses métadonnées en base."""
        document = await self._documents.get_by_id(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document introuvable")

        await self._s3.delete_file(document["s3_key"])
        await self._documents.delete_by_id(document_id)

        return {"id": document_id, "deleted": True}

    async def download_document(self, document_id: str) -> bytes:
        """Télécharge le contenu binaire d'un document depuis S3."""
        document = await self._documents.get_by_id(document_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Document introuvable")

        return await self._s3.download_file(document["s3_key"])