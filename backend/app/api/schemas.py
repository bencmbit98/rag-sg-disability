from typing import Optional
from pydantic import BaseModel


class HistoryMessage(BaseModel):
    role: str
    content: str


class QueryRequest(BaseModel):
    message: str
    history: list[HistoryMessage] = []


class SourceInfo(BaseModel):
    label: str
    url: str
    title: str
    snippet: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceInfo]
    is_in_scope: bool
    top_similarity_score: float
    refusal_reason: Optional[str] = None
    pages_searched: int
