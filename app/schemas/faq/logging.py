from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class FAQAction(str, Enum):
    created = "created"
    updated = "updated"
    deleted = "deleted"
    file_created = "file_created"      
    file_deleted = "file_deleted"


class QAPair(BaseModel):
    question: str
    answer: str


class FAQLogEntryBase(BaseModel):
    faq_id: str
    product_id: str
    admin: str
    timestamp: datetime
    action: FAQAction


class FAQCreatedLogEntry(FAQLogEntryBase):
    action: FAQAction = FAQAction.created
    question: str
    answer: str


class FAQUpdatedLogEntry(FAQLogEntryBase):
    action: FAQAction = FAQAction.updated
    before: QAPair
    after: QAPair


class FAQDeletedLogEntry(FAQLogEntryBase):
    action: FAQAction = FAQAction.deleted
    question: str
    answer: str


class FAQFileCreatedLogEntry(FAQLogEntryBase):
    """Création complète du fichier FAQ d'un produit (upload initial)."""
    action: FAQAction = FAQAction.file_created
    faq_id: str = "file"         
    item_count: int


class FAQFileDeletedLogEntry(FAQLogEntryBase):
    """Suppression complète du fichier FAQ d'un produit."""
    action: FAQAction = FAQAction.file_deleted
    faq_id: str = "file"
    filename: str
    item_count: int


FAQLogEntry = (
    FAQCreatedLogEntry
    | FAQUpdatedLogEntry
    | FAQDeletedLogEntry
    | FAQFileCreatedLogEntry
    | FAQFileDeletedLogEntry
)