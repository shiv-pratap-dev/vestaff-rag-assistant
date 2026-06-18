VeStaff RAG Assistant

A Retrieval-Augmented Generation (RAG) system for querying the AWS Customer Agreement using FastAPI, FAISS, HuggingFace embeddings, SQLite analytics, and Streamlit.

Built as part of the VeStaff Junior AI Developer Assignment. The system answers questions grounded in the AWS Customer Agreement PDF, tracks usage analytics in SQL, and provides an interactive chat interface with an analytics dashboard.

⸻
Demo Video: [[](https://www.dropbox.com/scl/fi/7c6xbjvmrhq7i62mxiy8p/AWS-RAG-Screenrecording.mp4?rlkey=nm9v5pfii68iixps14sqwlt5g&st=mvfc33a9&dl=0)]
⸻

Features

RAG Pipeline

* PDF ingestion via API
* Recursive document chunking
* SentenceTransformer embeddings
* FAISS vector search
* Top-K semantic retrieval
* Context-grounded answer generation
* Source chunk attribution
* Hallucination mitigation via constrained prompting

FastAPI Backend

* POST /ingest
* POST /ask
* GET /analytics
* Pydantic request/response validation
* Graceful error handling
* Session-aware chat history

SQL Analytics

Tracks every interaction and exposes:

* Most frequently asked questions
* Queries where no answer was found
* Average response latency

Additional analytics:

* Total queries
* Success rate
* Average retrieval confidence
* Recent queries
* Slowest queries

Streamlit Frontend

* Chat-style interface
* Automatic session management
* Source chunk inspection
* Analytics dashboard
* Document ingestion button

⸻

Architecture

                          ┌─────────────────┐
                          │ AWS Agreement   │
                          │      PDF        │
                          └────────┬────────┘
                                   │
                                   ▼
                         ┌──────────────────┐
                         │ PDF Loader       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Document Chunker │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Embeddings Model │
                         │ all-MiniLM-L6-v2 │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ FAISS Vector DB  │
                         └────────┬─────────┘
                                  │
                      User Query  │
                                  ▼
                         ┌──────────────────┐
                         │ Similarity Search│
                         │     Top-K=6      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Prompt Builder   │
                         │ + Chat History   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ HuggingFace LLM  │
                         │ Llama-3.1-8B     │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Generated Answer │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ SQLite Logging   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Analytics API    │
                         └──────────────────┘

⸻
Project Structure

vestaff-rag-assistant/
│
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
│
├── data/
│   └── aws_customer_agreement.pdf
│
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md

⸻

API Endpoints

POST /ingest

Processes the PDF, creates embeddings, and stores them in FAISS.

Response

{
  "message": "Document ingested successfully",
  "chunks_created": 43
}

⸻

POST /ask

Accepts a user question and returns an answer with supporting source chunks.

Request

{
  "session_id": "user-session-123",
  "question": "Can AWS suspend my account?"
}

Response

{
  "answer": "Yes, AWS can suspend your account...",
  "confidence_score": 0.57,
  "source_chunks": [...]
}

⸻

GET /analytics

Returns SQL-powered analytics.

Response

{
  "total_queries": 45,
  "success_rate": 91.11,
  "average_latency_ms": 2481.73,
  "average_confidence_score": 1.12,
  "most_frequent_questions": [...],
  "unanswered_queries": [...],
  "recent_queries": [...],
  "slowest_queries": [...]
}

⸻

Database Schema

CREATE TABLE query_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    confidence_score REAL,
    latency_ms REAL,
    answer_found INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

⸻

Design Decisions

Chunking Strategy

The AWS Customer Agreement is a legal document containing long clauses and section references.

A recursive text splitter was used to preserve semantic continuity while keeping chunks small enough for efficient retrieval.

* Chunk Size: 1000 characters
* Chunk Overlap: 200 characters

The overlap helps preserve context across clause boundaries and improves retrieval quality.

⸻

Embedding Model

sentence-transformers/all-MiniLM-L6-v2

Reasons:

* Lightweight
* Fast inference
* Strong semantic search performance
* Well supported within LangChain

⸻

Vector Store

FAISS

Reasons:

* Lightweight
* No external infrastructure required
* Fast local similarity search
* Ideal for assignment-scale RAG systems

⸻

Retrieval Strategy

Top-K = 6

After experimentation, Top-K of 6 provided a good balance between retrieval recall and prompt noise.

⸻

LLM Choice

Meta-Llama-3.1-8B-Instruct

Served through the HuggingFace Inference API.

Reasons:

* Strong instruction following
* Good context utilization
* No paid API required

⸻

Chat History

The system stores the previous three question-answer pairs per session and injects them into the prompt.

This enables contextual follow-up questions such as:

Can AWS suspend my account?
For what reasons?
What happens after that?

without requiring users to restate prior context.

⸻

Analytics Queries

Implemented analytics include:

Most Frequently Asked Questions

SELECT question, COUNT(*)
FROM query_logs
GROUP BY question
ORDER BY COUNT(*) DESC;

Unanswered Queries

SELECT question, COUNT(*)
FROM query_logs
WHERE answer_found = 0
GROUP BY question;

Average Latency

SELECT AVG(latency_ms)
FROM query_logs;

Additional metrics:

* Success Rate
* Average Confidence Score
* Recent Queries
* Slowest Queries

⸻

Setup Instructions

1. Clone Repository

git clone https://github.com/shiv-pratap-dev/vestaff-rag-assistant.git
cd vestaff-rag-assistant

⸻

2. Create Virtual Environment

Windows

python -m venv .venv
.venv\Scripts\activate

macOS / Linux

python3 -m venv .venv
source .venv/bin/activate

⸻

3. Install Dependencies

pip install -r requirements.txt

⸻

4. Create Environment File

Copy:

.env.example

to:

.env

and fill in your HuggingFace token.

Example:

HF_TOKEN=your_token_here

⸻

5. Start FastAPI

uvicorn main:app --reload

FastAPI will run at:

http://localhost:8000

Swagger documentation:

http://localhost:8000/docs

⸻

6. Start Streamlit

Open a second terminal:

streamlit run app/frontend/streamlit_app.py

Streamlit will run at:

http://localhost:8501

⸻

7. Ingest the Document

Use Swagger UI or the Streamlit button:

POST /ingest

This creates the FAISS vector store.

⸻

Running the Complete System

Terminal 1
│
└── uvicorn main:app --reload
Terminal 2
│
└── streamlit run app/frontend/streamlit_app.py

Then:

1. Open Streamlit
2. Click "Ingest AWS Agreement"
3. Start asking questions
4. View analytics dashboard

⸻

Testing

After building the system, 30+ test queries were executed against the API, including:

* Document-grounded questions
* Follow-up conversational questions
* Out-of-scope questions

This generated realistic analytics data for SQL aggregation and dashboard visualization.

⸻

Future Improvements

* Cross-encoder reranking
* Hybrid retrieval (BM25 + dense retrieval)
* Citation-aware answer generation
* Streaming responses
* PostgreSQL migration
* Multi-document support
* User authentication

⸻

Author

Shiv Pratap Singh

B.Tech Computer Science Engineering (AI/ML)
JECRC University, Jaipur

LinkedIn:[](https://www.linkedin.com/in/shiv-pratap-singh-734a7928b/)
