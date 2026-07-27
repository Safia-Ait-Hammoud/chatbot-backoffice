from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class FAQAction(str, Enum):
    created = "created"
    updated = "updated"
    deleted = "deleted"


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


FAQLogEntry = FAQCreatedLogEntry | FAQUpdatedLogEntry | FAQDeletedLogEntry