from fastapi import APIRouter, Depends, Form

from app.core.dependencies import get_document_indexing_service
from app.services.docs.document_indexing_service import DocumentIndexingService

router = APIRouter(prefix="/api/indexing", tags=["Indexing"])


@router.post("/")
async def indexing(
    document_id: str = Form(...),
    service: DocumentIndexingService = Depends(get_document_indexing_service),
):
    return await service.index_document(document_id)