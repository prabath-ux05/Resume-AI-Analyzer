from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from schemas.chat.messages import ChatMessageRequest, HistoryResponse
from services.chat.orchestrator import ChatOrchestrator
from services.memory.redis_memory import RedisMemoryService
from utils.rate_limiter import RateLimiter
from utils.logger import logger

router = APIRouter(prefix="/chat")
chat_orchestrator = ChatOrchestrator()

# Generous rate limit for chatting (e.g. 20 msgs per minute)
chat_rate_limit = RateLimiter(requests=20, window=60)

@router.post("/message", dependencies=[Depends(chat_rate_limit)])
async def chat_message_endpoint(request: ChatMessageRequest):
    """
    Streaming endpoint for general AI Assistant chat.
    """
    try:
        generator = chat_orchestrator.stream_message(
            message=request.message,
            file_hash=request.file_hash,
            session_id=request.session_id,
            is_interview=False
        )
        return StreamingResponse(generator, media_type="text/event-stream")
    except Exception as e:
        logger.error(f"Error in chat message endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to process chat message.")

@router.post("/interview", dependencies=[Depends(chat_rate_limit)])
async def chat_interview_endpoint(request: ChatMessageRequest):
    """
    Streaming endpoint for interview generation and practice.
    """
    try:
        generator = chat_orchestrator.stream_message(
            message=request.message,
            file_hash=request.file_hash,
            session_id=request.session_id,
            is_interview=True
        )
        return StreamingResponse(generator, media_type="text/event-stream")
    except Exception as e:
        logger.error(f"Error in chat interview endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to process interview message.")

@router.get("/history", response_model=HistoryResponse)
async def get_history(session_id: str):
    """
    Get the chat history for a given session.
    """
    try:
        history = await RedisMemoryService.get_history(session_id)
        # Filter out the hidden context messages before returning to frontend
        filtered_history = [
            msg for msg in history 
            if not (msg["role"] == "user" and "HIDDEN SYSTEM CONTEXT" in msg.get("content", ""))
            and not (msg["role"] == "assistant" and "Understood. I will use this resume context" in msg.get("content", ""))
        ]
        return HistoryResponse(session_id=session_id, messages=filtered_history)
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch chat history.")

@router.delete("/history")
async def delete_history(session_id: str):
    """
    Delete the chat history for a given session.
    """
    try:
        success = await RedisMemoryService.delete_history(session_id)
        return {"success": success, "session_id": session_id}
    except Exception as e:
        logger.error(f"Error deleting history: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete chat history.")
