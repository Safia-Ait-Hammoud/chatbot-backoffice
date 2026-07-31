from typing import Optional
from pydantic import BaseModel


class FAQUploadItem(BaseModel):
    """Une entrée Q/R du fichier JSON uploadé (sans id, à générer)"""
    category: Optional[str] = None
    question: str
    answer: str


class FAQFileMetadata(BaseModel):
    """Métadonnées du fichier FAQ d'un produit, stockées dans MongoDB (1 doc par produit)."""
    id: Optional[str] = None
    product_id: str
    filename: str
    s3_key: str
    admin: str
    item_count: int
    created_at: str


class FAQFileUploadResponse(BaseModel):
    product_id: str
    filename: str
    item_count: int
    created_at: str