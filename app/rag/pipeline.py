"""
RAG pipeline orchestration.

Flow:
Question
→ Retrieve relevant chunks
→ Build context
→ Build prompt
→ Generate answer
→ Return structured response
"""

from app.vector_store.vector_store import retrieve_chunks
from app.rag.prompt_builder import get_prompt
from app.rag.llm import llm


def answer_question(
    question: str,
    chat_history: str
):
    """
    Runs the complete RAG pipeline.

    Returns:
        dict containing:
        - answer
        - confidence_score
        - source_chunks
    """

    # Retrieve relevant chunks
    retrieved_results = retrieve_chunks(query=question)

    # Build context
    context = "\n\n".join(
        doc.page_content
        for doc, score in retrieved_results
    )

    # Build prompt
    prompt = get_prompt().format(
        chat_history=chat_history,
        context=context,
        question=question
    )

    # Generate answer
    answer = llm.invoke(prompt)

    # Best retrieval score
    # Smaller distance = better match

    confidence_score = (
        float(retrieved_results[0][1])
        if retrieved_results
        else 0.0
    )

    # Source chunks
    source_chunks = []

    for doc, score in retrieved_results:

        source_chunks.append(
            {
                "chunk_index": doc.metadata.get(
                    "chunk_index",
                    -1
                ),
                "score": float(score),
                "content": doc.page_content[:500]
            }
        )

    return {
        "answer": answer,
        "confidence_score": confidence_score,
        "source_chunks": source_chunks
    }