from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.core.dependencies import get_faq_file_service
from app.schemas.faq.management import FAQFile
from app.schemas.faq.upload import FAQFileUploadResponse
from app.services.faq.faq_file_service import FAQFileService
from app.services.faq.exceptions import (
    FAQFileAlreadyExistsError,
    FAQFileNotFoundError,
    InvalidFAQFileError,
    ProductNotFoundError,
)

router = APIRouter(prefix="/products/{product_id}/faq-file", tags=["faq-file"])


@router.post("", response_model=FAQFileUploadResponse, status_code=status.HTTP_201_CREATED)
async def create_faq_file(
    product_id: str,
    file: UploadFile = File(...),
    admin: str = Form(...),
    service: FAQFileService = Depends(get_faq_file_service),
) -> FAQFileUploadResponse:
    if not (file.filename or "").endswith(".json"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Le fichier doit être un .json")

    try:
        metadata = await service.create_faq_file(product_id, file, admin)
    except ProductNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except FAQFileAlreadyExistsError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except InvalidFAQFileError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc

    return FAQFileUploadResponse(
        product_id=metadata.product_id,
        filename=metadata.filename,
        item_count=metadata.item_count,
        created_at=metadata.created_at,
    )


@router.get("", response_model=FAQFile, status_code=status.HTTP_200_OK)
async def get_faq_file(
    product_id: str,
    service: FAQFileService = Depends(get_faq_file_service),
) -> FAQFile:
    try:
        return await service.get_faq_file(product_id)
    except FAQFileNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


from fastapi import APIRouter, Depends, HTTPException, Query, status

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_faq_file(
    product_id: str,
    admin: str = Query(..., description="Identifiant de l'admin à l'origine de l'action"),
    service: FAQFileService = Depends(get_faq_file_service),
) -> None:
    """Supprime entièrement le fichier FAQ d'un produit (S3 + Mongo + Qdrant)."""
    try:
        await service.delete_faq_file(product_id, admin)
    except FAQFileNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc