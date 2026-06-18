"""
Prompt builder for Retrieval-Augmented Generation (RAG).

This module combines retrieved document context, conversation history,
and the user's question into a structured prompt.
"""

from langchain_core.prompts import PromptTemplate


def get_prompt() -> PromptTemplate:
    """
    Returns the prompt template used for AWS Agreement QA.
    """

    template = """
You are an AI assistant specialized in answering questions about the AWS Customer Agreement.

Your task is to answer questions using ONLY the provided document context.

Rules:
- Use ONLY the information present in the document context.
- Do NOT use external knowledge.
- Do NOT make assumptions.
- Do NOT hallucinate facts.
- If the answer cannot be found in the context, respond exactly:

"I could not find the answer in the provided document."

- Use conversation history only to understand follow-up questions.
- Prioritize accuracy over completeness.
- Keep responses concise, clear, and professional.
- Do not mention retrieval, embeddings, chunks, or internal system details.

Conversation History:
{chat_history} 

Document Context:
{context}

User Question:
{question}

Answer:
"""

    return PromptTemplate(
        input_variables=[
            "chat_history",
            "context",
            "question"
        ],
        template=template
    )