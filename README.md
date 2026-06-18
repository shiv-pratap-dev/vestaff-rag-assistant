# VeStaff RAG – AWS Agreement Assistant

A Retrieval-Augmented Generation (RAG) system that allows users to ask questions about the AWS Customer Agreement and receive context-grounded answers with source references.

Built using FastAPI, FAISS, HuggingFace embeddings, SQLite analytics, and Streamlit.

Demo Video: [Watch Demo](https://www.dropbox.com/scl/fi/7c6xbjvmrhq7i62mxiy8p/AWS-RAG-Screenrecording.mp4?rlkey=nm9v5pfii68iixps14sqwlt5g&st=2qlxyoc8&dl=0)


---

## What it does

1. Ingests the AWS Customer Agreement PDF
2. Chunks and embeds document content
3. Stores embeddings in FAISS
4. Retrieves the most relevant sections for a query
5. Builds a grounded prompt using retrieved context
6. Generates answers using Llama 3.1
7. Logs every interaction into SQLite
8. Exposes analytics through SQL-powered APIs

The system also supports conversational follow-up questions by maintaining the previous three question-answer pairs within a session.

---

## Tech Stack

Backend: FastAPI

Frontend: Streamlit

Vector Store: FAISS

Embeddings: SentenceTransformers (all-MiniLM-L6-v2)

LLM: Meta Llama 3.1 8B Instruct (HuggingFace Inference API)

Database: SQLite

Language: Python

---

## Architecture

User

↓

Streamlit UI

↓

FastAPI

↓

PDF Loader

↓

Document Chunking

↓

Embeddings

↓

FAISS Semantic Retrieval

↓

Prompt Builder + Chat History

↓

Llama 3.1

↓

Answer + Source Chunks

↓

SQLite Logging

↓

Analytics Dashboard

---

## Features

### RAG Pipeline

• PDF ingestion through API

• Recursive document chunking

• Semantic retrieval using FAISS

• Top-K retrieval

• Context-grounded generation

• Source chunk attribution

• Follow-up conversational support

### FastAPI Backend

• POST /ingest

• POST /ask

• GET /analytics

• Pydantic validation

• Graceful error handling

### SQL Analytics

Tracks:

• Total queries

• Success rate

• Average latency

• Average confidence score

• Most frequent questions

• Unanswered queries

• Recent queries

• Slowest queries

### Streamlit Frontend

• Chat interface

• Automatic session management

• Source chunk viewer

• Analytics dashboard

• One-click document ingestion

---

## Project Structure

    vestaff-rag-assistant/
    ├── app/
    │   ├── core/
    │   │   └── config.py
    │   │
    │   ├── db/
    │   │   ├── database.py
    │   │   └── queries.py
    │   │
    │   ├── frontend/
    │   │   └── streamlit_app.py
    │   │
    │   ├── rag/
    │   │   ├── loader.py
    │   │   ├── chunker.py
    │   │   ├── embeddings.py
    │   │   ├── llm.py
    │   │   ├── pipeline.py
    │   │   └── prompt_builder.py
    │   │
    │   ├── routes/
    │   │   └── routes.py
    │   │
    │   ├── schemas/
    │   │   └── schemas.py
    │   │
    │   └── vector_store/
    │       └── vector_store.py
    │
    ├── assets/
    ├── data/
    │   └── aws_customer_agreement.pdf
    │
    ├── .env.example
    ├── .gitignore
    ├── main.py
    ├── requirements.txt
    └── README.md

---

## API Endpoints

### POST /ingest

Processes the AWS Agreement PDF and creates the FAISS vector store.

### POST /ask

Accepts a question and returns:

• Answer

• Confidence score

• Source chunks

### GET /analytics

Returns SQL-powered usage analytics.

---

## Example Questions

• Can AWS suspend my account?

• For what reasons?

• What happens after termination?

• Who owns my content?

• Can AWS access my data?

• What happens if I fail to make payments?

• What are my responsibilities under the agreement?

These demonstrate both direct retrieval and conversational follow-up behavior.

---

## Run Locally

Clone the repository:

    git clone https://github.com/shiv-pratap-dev/vestaff-rag-assistant.git

    cd vestaff-rag-assistant

Create environment file:

    cp .env.example .env

Add your HuggingFace token:

    HF_TOKEN=your_token_here

Install dependencies:

    pip install -r requirements.txt

Start FastAPI:

    uvicorn main:app --reload

Swagger:

    http://localhost:8000/docs

Start Streamlit in a separate terminal:

    streamlit run app/frontend/streamlit_app.py

Open:

    http://localhost:8501

Click:

    Ingest AWS Agreement

Then start chatting with the document.

---

## Important Note

As required by the assignment, Streamlit runs as a separate process from FastAPI and communicates with the backend through HTTP requests.

    Streamlit → HTTP → FastAPI

---

## Testing

The system was tested using 30+ queries including:

• Answerable document-based questions

• Multi-turn follow-up questions

• Out-of-scope questions

This generated realistic analytics data for evaluating retrieval quality and system performance.

---

## Future Improvements

• Cross-encoder reranking

• Hybrid retrieval (BM25 + dense retrieval)

• Streaming responses

• Multi-document support

• PostgreSQL analytics backend

• Authentication and user management

---

## Author

Shiv Pratap Singh

B.Tech Computer Science Engineering (AI/ML)

JECRC University, Jaipur

LinkedIn:
https://www.linkedin.com/in/shiv-pratap-singh-734a7928b/
