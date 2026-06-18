# main.py

from fastapi import FastAPI

from app.api.routes import router
from app.db.database import init_db


init_db()

app = FastAPI(
    title="VeStaff RAG API"
)

app.include_router(router)