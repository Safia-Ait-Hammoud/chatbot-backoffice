from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_faq_management_service
from app.schemas.faq.management import (
    FAQCreateRequest,
    FAQDeleteRequest,
    FAQItem,
    FAQUpdateRequest,
)
from app.services.faq.faq_management_service import FAQManagementService, FAQNotFoundError

router = APIRouter(prefix="/products/{product_id}/faq", tags=["faq-management"])


@router.post("", response_model=FAQItem, status_code=status.HTTP_201_CREATED)
def create_faq(
    product_id: str,
    request: FAQCreateRequest,
    service: FAQManagementService = Depends(get_faq_management_service),
) -> FAQItem:
    return service.create_faq(product_id, request)


@router.put("/{faq_id}", response_model=FAQItem)
def update_faq(
    product_id: str,
    faq_id: str,
    request: FAQUpdateRequest,
    service: FAQManagementService = Depends(get_faq_management_service),
) -> FAQItem:
    try:
        return service.update_faq(product_id, faq_id, request)
    except FAQNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{faq_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faq(
    product_id: str,
    faq_id: str,
    request: FAQDeleteRequest,
    service: FAQManagementService = Depends(get_faq_management_service),
) -> None:
    try:
        service.delete_faq(product_id, faq_id, request)
    except FAQNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc