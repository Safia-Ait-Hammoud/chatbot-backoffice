from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.core.dependencies import get_document_service, get_document_indexing_service
from app.services.docs.document_service import DocumentService
from app.services.docs.document_indexing_service import DocumentIndexingService

router = APIRouter(prefix="/api/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(
    project_id: str = Form(...),
    file: UploadFile = File(...),
    filename: Optional[str] = Form(None),
    service: DocumentService = Depends(get_document_service),
    service_indexing: DocumentIndexingService = Depends(get_document_indexing_service),
    
):
    result = await service.add_file(file, project_id, filename)
    index = await service_indexing.index_document(result.id)
    message = "l'indexation a été effectuée avec succès" if index else "l'indexation a échoué"
    return {"data": result, "message": message}


@router.get("/list/{project_id}")
async def list_documents(
    project_id: str,
    service: DocumentService = Depends(get_document_service),
):
    documents = await service.list_documents(project_id)
    return {"project": project_id, "documents": documents}


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    service: DocumentService = Depends(get_document_service),
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

    return result


# @router.get("/download/{document_id}")
# async def download_document(
#     document_id: str,
#     service: DocumentService = Depends(get_document_service),
# ):
#     try:
#         pdf_bytes = await service.download_document(document_id)
#         return Response(content=pdf_bytes, media_type="application/pdf")
#     except FileNotFoundError as e:
#         return {"error": str(e)}