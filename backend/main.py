from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.resume_routes import router as resume_router
from api.chat.routes import router as chat_router
from utils.logger import logger
from database.redis import init_redis, close_redis
from database.qdrant import init_qdrant

app = FastAPI(
    title="Resume AI Analyzer API",
    description="Backend API for parsing and analyzing resumes using Gemini.",
    version="2.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from database.postgres import init_db

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

# Include routes
app.include_router(resume_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Elevora AI API"}
