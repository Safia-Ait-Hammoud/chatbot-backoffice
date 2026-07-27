from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: str
    filename: str
    project_id: str
    s3_key: str
    url: str


    class Config:
            from_attributes = True