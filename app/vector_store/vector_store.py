"""
Vector Store utility module
This module handles saving, loading and retrieving
from the FIASS vector store
"""

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import settings

VECTOR_DIR = "vectorstores" # the exact directory where FAISS index persists

# Global embedding model used across the application
embedder = HuggingFaceEmbeddings(
    model_name = settings.EMBEDDING_MODEL
)

def save_vector_store(vector_store: FAISS)-> None:
    vector_store.save_local(VECTOR_DIR)

def load_vector_store() ->FAISS:
    # LOAD the persisted FAISS vector store from VECTOR_DIR

    return FAISS.load_local(
        VECTOR_DIR,
        embeddings= embedder,
        allow_dangerous_deserialization=True # this forces acknowledgment of pickle security risk
    )

def retrieve_chunks(query: str,
        k: int = settings.TOP_K):
  
    # Retrieves the most relevant chunks along with their similarity scores
    # Returns: List[Tuple[Document, float]]

    vs = load_vector_store()

    results = vs.similarity_search_with_score(
        query= query,
        k = k
    )

    return results


    