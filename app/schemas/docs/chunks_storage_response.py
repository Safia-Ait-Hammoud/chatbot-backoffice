from pydantic import BaseModel

class ChunksStorageResponse(BaseModel):
    collection: str
    inserted_count: int

    class Config:
        from_attributes = True



