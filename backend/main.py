from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.resume_routes import router as resume_router
from api.chat.routes import router as chat_router

from utils.logger import logger
from database.redis import init_redis, close_redis
from database.qdrant import init_qdrant
from database.postgres import init_db


app = FastAPI(
    title="Resume AI Analyzer API",
    description="Backend API for parsing and analyzing resumes using Groq.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up application...")
    await init_db()
    await init_redis()
    init_qdrant()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application...")
    await close_redis()


app.include_router(resume_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"status": "backend running"}


@app.head("/")
async def head_root():
    return None