from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_faq_indexing_service
from app.schemas.faq.indexingFaq import FAQCreatedEvent, FAQDeletedEvent, FAQUpdatedEvent
from app.services.faq.faq_indexing_service import FAQIndexingService

router = APIRouter(prefix="/faq/events", tags=["faq-indexing"])


@router.post("/created", status_code=status.HTTP_204_NO_CONTENT)
def created(
    event: FAQCreatedEvent,
    service: FAQIndexingService = Depends(get_faq_indexing_service),
) -> None:
    service.handle_created(event)


@router.put("/updated", status_code=status.HTTP_204_NO_CONTENT)
def updated(
    event: FAQUpdatedEvent,
    service: FAQIndexingService = Depends(get_faq_indexing_service),
) -> None:
    service.handle_updated(event)


@router.delete("/deleted", status_code=status.HTTP_204_NO_CONTENT)
def deleted(
    event: FAQDeletedEvent,
    service: FAQIndexingService = Depends(get_faq_indexing_service),
) -> None:
    service.handle_deleted(event)