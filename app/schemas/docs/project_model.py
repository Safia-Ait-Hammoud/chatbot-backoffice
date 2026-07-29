from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class ProjectCreate(BaseModel):
    """Payload pour créer un projet"""
    name: str


class ProjectModel(ProjectCreate):
    """Représentation stockée en base """
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ProjectResponse(BaseModel):
    """Réponse renvoyée au client par l'API"""
    id: str
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)