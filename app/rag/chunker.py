"""
Chunking utility module
This module splits the AWS Customer Agreement pdf's extracted raw text 
into overlapping chunks for semantic retrieval
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def chunk_document(
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 100

) -> list[Document]:
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size= chunk_size,
        chunk_overlap = chunk_overlap,
        separators= ["\n\n", "\n", " ", ""]
    )

    chunks = splitter.create_documents([text])

    #attaching the metadat: chunk index for traceability
    for i , chunk in enumerate(chunks):
        chunk.metadata['chunk_index'] = i
    
    return chunks
        