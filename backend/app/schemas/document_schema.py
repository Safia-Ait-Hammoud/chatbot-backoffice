
from pydantic import BaseModel

class DocumentUploadResponse(BaseModel):
    success: bool
    message: str
    file_name: str
    project_id: str
    bucket_name: str
    s3_key: str
