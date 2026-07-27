from fastapi import APIRouter, UploadFile, File, Form, Depends,Query , BackgroundTasks
from fastapi.responses import Response
from core.dependencies import get_document_service
from core.dependencies import get_document_indexing_service
from services.document_service import DocumentService
from services.document_indexing_service import DocumentIndexingService
from typing import Optional

router = APIRouter(prefix="/api/documents", tags=["Documents"])

@router.post("/upload")
async def upload_document(
    project_id: str = Form(...),
    file: UploadFile = File(...),
    filename: Optional[str] = Form(None),
    service = Depends(get_document_service),
    service_indexing: DocumentIndexingService = Depends(get_document_indexing_service),
):
    result = await service.add_file(file, project_id, filename)
    index = await service_indexing.index_document(result.id)
    if index :
        message ="l'indexation effectuer avec succès"
    else :
        message ="l'indexation a échoué"
    return {
        "data": result,
        "message": message
    }




@router.get("/list/{project_id}")
async def list_documents(
    project_id: str ,
    service = Depends(get_document_service),
    ):
    documents = await service.list_documents(project_id)
    return {"project": project_id, "documents": documents}


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    service = Depends(get_document_service),
):
    result = await service.delete_document(document_id)
    return {"data": result}




@router.put("/")
async def update_document(
    document_id: str = Form(...),
    file: Optional[UploadFile] = File(None),
    filename: Optional[str] = Form(None),
    service: DocumentService = Depends(get_document_service),
    service_indexing: DocumentIndexingService = Depends(get_document_indexing_service),
):
    result = await service.update_doc(document_id, file, filename)

    if file is not None:
        await service_indexing.reindex_document(document_id)
        message = "Document mis à jour et réindexé avec succès."
    else:
        message = "Document mis à jour. Réindexation non nécessaire."

    return {
        "data": result,
        "message": message,
    }
   

#@router.get("/download/{document_id}")
#async def download_document(
#    document_id: str,
#    service: DocumentService = Depends(get_document_service),
#):
#   try:
#        pdf_bytes = await service.download_document(document_id)
#        return Response(content=pdf_bytes , media_type="application/pdf")
#
#    except FileNotFoundError as e:
#        return {"error": str(e)}
    

