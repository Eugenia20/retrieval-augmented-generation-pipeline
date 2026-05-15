from pydantic import BaseModel
from typing import List


class QueryRequest(BaseModel):
    query: str


class Source(BaseModel):
    document_id: int
    filename: str


class QueryResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[Source]