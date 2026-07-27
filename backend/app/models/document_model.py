from datetime import datetime
from pydantic import BaseModel, Field

class DocumentCreate(BaseModel):
    project_id: str
    filename: str

class DocumentModel(DocumentCreate):
    s3_key: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    url:str

class DocumentOut(DocumentModel):
    id: str