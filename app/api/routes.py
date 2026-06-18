"""
API routes.
"""

import os
import time

from fastapi import (
    APIRouter,
    HTTPException
)

from app.rag.loader import load_pdf
from app.rag.chunker import chunk_document
from app.rag.embeddings import create_vector_store
from app.schemas.schemas import (IngestResponse,
                                 AskRequest, AskResponse)

from app.vector_store.vector_store import (
    save_vector_store
)

from app.core.config import settings

from app.rag.pipeline import answer_question

from app.db.queries import (
    log_query,
    get_total_queries,
    get_success_rate,
    get_average_latency,
    get_average_confidence,
    get_most_frequent_questions,
    get_unanswered_queries,
    get_recent_queries,
    get_slowest_queries,
    get_chat_history
)


router = APIRouter()
@router.post(
    "/ingest",
    response_model=IngestResponse
)
def ingest_document():

    try:
        text = load_pdf(
            settings.FILE_PATH
        )
        chunks = chunk_document(
            text
        )
        vector_store = create_vector_store(
            chunks
        )
        save_vector_store(
            vector_store
        )
        return IngestResponse(
            message="Document ingested successfully",
            chunks_created=len(chunks)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}"
        )

@router.post(
    "/ask",
    response_model=AskResponse
)
def ask_question(payload: AskRequest):

    """
    Ask a question about the document.
    """

    start_time = time.time()

    if not payload.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
    )

    # Load previous conversation
    history_rows = get_chat_history(
        payload.session_id
    )

    chat_history = ""

    for question, answer in history_rows:

        chat_history += (
            f"User: {question}\n"
            f"Assistant: {answer}\n\n"
        )

    if not os.path.exists(
        settings.VECTOR_STORE_PATH
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "No document has been ingested yet. "
                "Please call /ingest first."
            )
        )
    # Run RAG pipeline
    result = answer_question(
        question=payload.question,
        chat_history=chat_history
    )


    # Calculate latency
    latency_ms = (
        time.time() - start_time
    ) * 1000

    # Determine whether answer was found
    answer_found = (
        "I could not find the answer"
        not in result["answer"]
    )


    # Store interaction
    log_query(
        session_id=payload.session_id,
        question=payload.question,
        answer=result["answer"],
        confidence_score=result["confidence_score"],
        latency_ms=latency_ms,
        answer_found=answer_found
    )

    return result


@router.get("/analytics")
def analytics():

    """
    Returns analytics dashboard data.
    """

    return {

        "total_queries":
        get_total_queries(),

        "success_rate":
        get_success_rate(),

        "average_latency_ms":
        get_average_latency(),

        "average_confidence_score":
        get_average_confidence(),

        "most_frequent_questions":
        get_most_frequent_questions(),

        "unanswered_queries":
        get_unanswered_queries(),

        "recent_queries":
        get_recent_queries(),

        "slowest_queries":
        get_slowest_queries()

    }