"""
Embeddings utility module
This module generates embeddings for document chunks
and creates a FAISS vector store for semantic retrieval
"""
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from app.core.config import settings

#global embedding model that is used acrossed this application
embedder = HuggingFaceEmbeddings(
    model_name = settings.EMBEDDING_MODEL
)

def create_vector_store(chunks: list[Document]) -> FAISS:
    """
    Creates a FAISS vector store from chunked documents
    here:
        chunks (list[Document]): Chunked document objects,
    and the function returns:
        FAISS Vector store containing embedded chunks.
    """

    vector_store = FAISS.from_documents(
        documents= chunks,
        embedding= embedder
    )

    return vector_store