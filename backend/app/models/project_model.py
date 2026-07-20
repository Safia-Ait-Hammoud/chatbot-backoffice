from datetime import datetime

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str


class ProjectModel(ProjectCreate):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ProjectOut(ProjectModel):
    id: str
    