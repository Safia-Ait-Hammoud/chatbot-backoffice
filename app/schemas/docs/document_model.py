from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class DocumentCreate(BaseModel):
    """Payload pour créer un document"""
    project_id: str
    filename: str


class DocumentModel(DocumentCreate):
    """Représentation stockée en base"""
    s3_key: str
    url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DocumentResponse(BaseModel):
    """Réponse renvoyée au client par l'API"""
    id: str
    filename: str
    project_id: str
    s3_key: str
    url: str

    model_config = ConfigDict(from_attributes=True)