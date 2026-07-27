from fastapi import HTTPException, UploadFile , BackgroundTasks
from services.s3_service import S3Service
from models.document_model import DocumentModel 
from repositories.document_repository import DocumentRepository
from repositories.project_repository import ProjectRepository
from schemas.document_response import DocumentResponse


class DocumentService:
    """
        Service métier gérant le cycle de vie des documents :
        upload, mise à jour, suppression, téléchargement et consultation.
 
    """

    def __init__(self):
        self.s3_service = S3Service()
        self.document_repository = DocumentRepository()
        self.project_repository = ProjectRepository()


    async def add_file(self, file: UploadFile, project_id: str , filename:str ) -> DocumentResponse:
        """
         Upload un nouveau fichier sur S3 et enregistre ses métadonnées en base .
        """

        project = await self.project_repository.get_by_id(project_id)

        if not project:
            raise HTTPException(
                status_code=404,
                detail="Projet introuvable"
            )

        result = await self.s3_service.upload_file(file, project["name"])

        document = DocumentModel(
            project_id=project_id,
            filename= filename if filename else result["filename"], 
            s3_key=result["s3_key"],
            url=result["url"] ,
            
        )

        try:
            document_id = await self.document_repository.create(document)
        except Exception as e:
            await self.s3_service.delete_file(result["s3_key"])
            raise HTTPException(
                status_code=500,
                detail=f"Erreur MongoDB : {str(e)}"
            )
            
        return DocumentResponse(
            id=document_id,
            project_id=project_id,
            filename=document.filename,
            s3_key=document.s3_key,
            url=document.url,
        )
        
        
    
    
    async def update_doc(self, document_id: str, file: UploadFile = None, filename: str = None) -> DocumentResponse:
        
        """
             Met à jour un document existant : le nom, le fichier, ou les deux.
        """

        if not file and not filename:
            raise HTTPException(status_code=400, detail="Aucune modification fournie (file ou filename requis)")

        old_doc = await self.document_repository.get_by_id(document_id)
        if not old_doc:
            raise HTTPException(status_code=404, detail="Document introuvable")

        project = await self.project_repository.get_by_id(old_doc["project_id"])
        if not project:
            raise HTTPException(status_code=404, detail="Projet introuvable")

        new_filename = old_doc["filename"]
        new_s3_key = old_doc["s3_key"]
        new_url = old_doc["url"]

        if file:
            result = await self.s3_service.upload_file(file, project["name"])
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
            updated = await self.document_repository.update(document_id, new_doc)
            if not updated:
                raise HTTPException(status_code=404, detail="Document introuvable ou non modifié")
        except HTTPException:
            if file:
                await self.s3_service.delete_file(new_s3_key)
            raise
        except Exception as e:
            if file:
                await self.s3_service.delete_file(new_s3_key)
            raise HTTPException(status_code=500, detail=f"Erreur MongoDB : {str(e)}")

        if file:
            # L'update en base a réussi : on peut supprimer l'ancien fichier

            try:
                await self.s3_service.delete_file(old_doc["s3_key"])
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Erreur lors de la suppression du fichier S3 : {str(e)}"
                )

        return DocumentResponse(
            id=old_doc["id"],
            project_id=new_doc.project_id,
            filename=new_doc.filename,
            s3_key=new_doc.s3_key,
            url=new_doc.url,
        )


    async def list_documents(self, project_id: str) -> list[DocumentResponse]:

        docs= await self.document_repository.list_by_project(project_id)
        return DocumentResponse.model_validate(docs)


    async def get_document_by_id(self, document_id: str) -> DocumentResponse:
        doc = await self.document_repository.get_by_id(document_id)  
        if not doc :                                            
            raise HTTPException(                                       
                status_code=404,
                detail="Document introuvable"
            )
        return DocumentResponse.model_validate(doc)

    async def get_documents_by_project_id(self, project_id: str) -> list[DocumentResponse]:
        docs = await self.document_repository.list_by_project(project_id)
        return DocumentResponse.model_validate(docs)


    async def delete_document(self, document_id: str):
        """
         Supprime un document : son fichier sur S3 puis ses métadonnées en base.
        """
        
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
        """
         Télécharge le contenu binaire d'un document depuis S3.
        """

        document = await self.document_repository.get_by_id(document_id)

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document introuvable"
            )

        return await self.s3_service.download_file(document["s3_key"])



    

    
    
    