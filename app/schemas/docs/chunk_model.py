import pydantic
from datetime import datetime, timezone


class ParentChildMetadata(pydantic.BaseModel):
    H1: str | None = None
    H2: str


class ParentModel(pydantic.BaseModel):
    id: str = pydantic.Field(alias="_id")  # = parent_id généré pendant le chunking
    parent_index: int
    content: str
    metadata: ParentChildMetadata
    project_id: str
    document_id: str
    created_at: datetime = pydantic.Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = pydantic.ConfigDict(populate_by_name=True)


class ChildPayload(pydantic.BaseModel):
    project_id: str
    document_id: str
    parent_id: str
    parent_index: int
    child_index: int
    content: str

class SparseVectorModel(pydantic.BaseModel):
    indices: list[int]
    values: list[float]


class ChildVectors(pydantic.BaseModel):
    dense: list[float] # pour la recherche simentic 
    bm25: SparseVectorModel # pour la recherche BM25



class ChildModel(pydantic.BaseModel):
    child_id: str
    vectors: ChildVectors
    payload: ChildPayload

