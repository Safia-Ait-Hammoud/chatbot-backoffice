from fastapi import APIRouter, UploadFile, File, Form, Depends,Query
from fastapi.responses import Response
from services.document_service import DocumentService

router = APIRouter(prefix="/api/documents", tags=["Documents"])


def get_document_service():
    return DocumentService()


@router.post("/upload")
async def upload_document(
    project_id: str = Form(...),
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service),
):
    result = await service.add_file(file, project_id)
    return {
        "data": result,
    }

@router.get("/list/{project_id}")
async def list_documents(
    project_id: str ,
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
    

