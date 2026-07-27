from typing import Optional
from pydantic import BaseModel, Field


class FAQItem(BaseModel):
    """Représente une entrée FAQ telle que stockée dans le fichier S3"""

    id: str = Field(..., description="UUID de la FAQ (faq_id)")
    category: Optional[str] = Field(
        default=None, description="Catégorie libre (ex: 'compte')"
    )
    question: str
    answer: str


class FAQFile(BaseModel):
    """Représente le contenu complet du fichier faq_{product_id}.json."""

    product_id: str
    product_name: Optional[str] = Field(default=None)
    product_url: Optional[str] = Field(default=None)
    items: list[FAQItem] = Field(default_factory=list)


class FAQCreateRequest(BaseModel):
    """Corps de requête pour POST /products/{product_id}/faq."""

    category: Optional[str] = None
    question: str
    answer: str
    admin: str = Field(..., description="Identifiant de l'admin à l'origine de l'action")


class FAQUpdateRequest(BaseModel):
    """
    Corps de requête pour PUT /products/{product_id}/faq/{faq_id}
    """
    category: Optional[str] = None
    question: Optional[str] = None
    answer: Optional[str] = None
    admin: str = Field(..., description="Identifiant de l'admin à l'origine de l'action")


class FAQDeleteRequest(BaseModel):
    """Corps de requête pour DELETE /products/{product_id}/faq/{faq_id}"""

    admin: str = Field(..., description="Identifiant de l'admin à l'origine de l'action")