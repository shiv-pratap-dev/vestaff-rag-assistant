"""
Pydantic request/response schemas.
"""

from pydantic import BaseModel
from pydantic import Field

class IngestResponse(BaseModel):
    message: str
    chunks_created: int

class AskRequest(BaseModel):
    """
    Incoming user question.
    """

    session_id: str
    question: str = Field(
        min_length= 1
    )


class SourceChunk(BaseModel):
    """
    Source chunk returned to the user.
    """

    chunk_index: int
    score: float
    content: str


class AskResponse(BaseModel):
    """
    RAG answer response.
    """

    answer: str
    confidence_score: float
    source_chunks: list[SourceChunk]


class AnalyticsResponse(BaseModel):
    """
    Analytics dashboard response.
    """

    total_queries: int

    success_rate: float

    average_latency_ms: float

    average_confidence_score: float

    most_frequent_questions: list

    unanswered_queries: list

    recent_queries: list

    slowest_queries: list