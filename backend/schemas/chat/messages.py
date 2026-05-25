from pydantic import BaseModel, Field

from typing import List, Dict, Any

class ChatMessageRequest(BaseModel):
    message: str = Field(..., description="The user's message to the AI assistant")
    file_hash: str = Field(..., description="The SHA256 hash of the uploaded resume to fetch context")
    session_id: str = Field(..., description="Unique ID for maintaining conversation history in Redis")

class ChatResponse(BaseModel):
    response: str = Field(..., description="The AI assistant's response")
    session_id: str = Field(..., description="The session ID to continue the conversation")
    
class HistoryResponse(BaseModel):
    session_id: str
    messages: List[Dict[str, Any]]
