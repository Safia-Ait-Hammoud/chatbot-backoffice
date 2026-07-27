from pydantic import BaseModel

class ProjectResponse(BaseModel):
    id:str
    name:str
    created_at:str

    class Config:
        from_attributes = True