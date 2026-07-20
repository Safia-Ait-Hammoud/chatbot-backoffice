from fastapi import APIRouter, UploadFile, File, Form, Depends,Query
from fastapi.responses import Response
from services.indexing_service import IndexingService


router = APIRouter(prefix="/api/indexing", tags=["Indexing"])


def get_indexing_service():
    return IndexingService()


@router.post("/")
async def prepare_document(
    documnet_id: str = Form(...),
    service: IndexingService = Depends(get_indexing_service),
): 
    result = await service.prepare_document(documnet_id)
    return result

