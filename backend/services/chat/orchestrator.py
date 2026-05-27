import json
import os
from groq import AsyncGroq
from services.context.resume_context import ResumeContextService
from services.memory.redis_memory import RedisMemoryService
from prompts.chat.assistant import ASSISTANT_SYSTEM_PROMPT
from utils.logger import logger

class ChatOrchestrator:
    """
    Coordinates the Chat logic, pulling context from ResumeContextService
    and memory from RedisMemoryService before invoking Gemini.
    """
    def __init__(self, model_name: str = "llama-3.1-8b-instant"):

        self.model_name = model_name

        self.client = AsyncGroq(
            api_key=os.getenv("GROQ_API_KEY")
    )

    async def _manage_token_window(self, raw_history: list) -> list:
        """
        Manages the rolling token window. If history exceeds 12 messages,
        extracts the middle block and summarizes it, preserving the system 
        context (first 2 messages) and recent history (last 6 messages).
        """
        if len(raw_history) <= 12:
            return raw_history
            
        logger.info(f"History length {len(raw_history)} exceeds threshold. Summarizing middle block...")
        
        system_context = raw_history[:2]
        recent_history = raw_history[-6:]
        middle_block = raw_history[2:-6]
        
        # Build prompt for summarization
        transcript = ""
        for msg in middle_block:
            role = msg["role"]
            text = msg["parts"][0]
            transcript += f"[{role.upper()}]: {text}\n"
            
        summary_prompt = (
            "You are an AI assistant memory manager. Please compactly summarize the following conversation block.\n"
            "Focus strictly on the user's career goals, preferences, topics discussed, and conclusions reached.\n"
            "Keep it to 2-3 short bullet points. Do not include pleasantries.\n\n"
            f"CONVERSATION LOG:\n{transcript}"
        )
        
        try:

            transcript_messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an AI assistant memory manager. "
                        "Summarize the conversation compactly. "
                        "Focus only on career goals, preferences, "
                        "topics discussed, and conclusions reached. "
                        "Keep it short with 2-3 bullet points."
                    )
                },
                {
                    "role": "user",
                    "content": transcript
                }
            ]

            summary_response = await self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=transcript_messages,
                temperature=0.3
            )

            summary_text = (
                summary_response
                .choices[0]
                .message
                .content
            )

            summary_node = {
                "role": "user",
                "parts": [
                    f"SYSTEM NOTE (Hidden): "
                    f"The conversation prior to this point "
                    f"was summarized to save memory:\n{summary_text}"
                ]
            }

            ack_node = {
                "role": "model",
                "parts": [
                    "I have logged the summary "
                    "of our previous conversation."
                ]
            }

            return (
                system_context
                + [summary_node, ack_node]
                + recent_history
            )

        except Exception as e:

            logger.error(f"Failed to summarize history: {e}")

            return system_context + recent_history

    async def process_message(self, message: str, file_hash: str, session_id: str) -> str:
        """
        Process the user's message, inject resume context if starting fresh,
        maintain history, and return the AI response.
        """
        logger.info(f"Processing chat message for session: {session_id}")
        
        # 1. Fetch History
        raw_history = await RedisMemoryService.get_history(session_id)
        
        # 2. Inject Context if this is a new conversation
        if not raw_history:
            resume_context_string = await ResumeContextService.get_context(file_hash)
            if resume_context_string:
                context_message = (
                    "HIDDEN SYSTEM CONTEXT (Do not mention this message to the user):\n"
                    f"Here is the user's resume data:\n{resume_context_string}"
                )
                raw_history.append({"role": "user", "parts": [context_message]})
                raw_history.append({"role": "model", "parts": ["Understood. I will use this resume context to answer the user's career questions."]})
        
        # 2.5 Manage token window (Summarize if too long)
        raw_history = await self._manage_token_window(raw_history)
        
        # 3. Format history for Gemini API
        gemini_history = []
        for msg in raw_history:
            gemini_history.append({
                "role": msg["role"],
                "parts": msg["parts"]
            })

        # 4. Start Chat and Send Message
        messages = []

        for msg in gemini_history:
            messages.append({
                "role": msg["role"],
                "content": msg["parts"][0]
            })

        messages.append({
            "role": "user",
            "content": message
        })

        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.5
        )

        response_text = response.choices[0].message.content
        
        # 5. Append new messages to our raw history for saving
        raw_history.append({"role": "user", "parts": [message]})
        raw_history.append({"role": "model", "parts": [response_text]})
        
        # 6. Save back to Redis
        await RedisMemoryService.save_history(session_id, raw_history)
        
        return response_text

    async def stream_message(self, message: str, file_hash: str, session_id: str, is_interview: bool = False):
        """
        Process the user's message and yield a streaming response.
        """
        logger.info(f"Streaming chat message for session: {session_id}, is_interview: {is_interview}")
        
        # 1. Fetch History
        raw_history = await RedisMemoryService.get_history(session_id)
        
        # 2. Inject Context if this is a new conversation
        if not raw_history:
            resume_context_string = await ResumeContextService.get_context(file_hash)
            if resume_context_string:
                context_message = (
                    "HIDDEN SYSTEM CONTEXT (Do not mention this message to the user):\n"
                    f"Here is the user's resume data:\n{resume_context_string}"
                )
                raw_history.append({"role": "user", "parts": [context_message]})
                
                initial_ack = "Understood. I will use this resume context to answer the user's career questions."
                if is_interview:
                    from prompts.interview.questions import INTERVIEW_QUESTIONS_PROMPT
                    initial_ack = f"Understood. I will use this resume context to conduct a technical interview.\n{INTERVIEW_QUESTIONS_PROMPT}"
                
                raw_history.append({"role": "model", "parts": [initial_ack]})
        
        # 2.5 Manage token window (Summarize if too long)
        raw_history = await self._manage_token_window(raw_history)
        
        # 3. Format history for Gemini API
        gemini_history = []
        for msg in raw_history:
            gemini_history.append({
                "role": msg["role"],
                "parts": msg["parts"]
            })

        # 4. Start Chat and Send Message (Streaming)
        import asyncio
        chat_session = self.model.start_chat(history=gemini_history)
        
        full_response = ""
        
        try:
            # Enforce 15s timeout for the stream to establish
            response_stream = await asyncio.wait_for(
                chat_session.send_message_async(message, stream=True),
                timeout=15.0
            )
            
            async for chunk in response_stream:
                if chunk.text:
                    full_response += chunk.text
                    yield chunk.text
                    
        except asyncio.TimeoutError:
            logger.error(f"Gemini API timeout during chat stream for session {session_id}.")
            error_msg = "\n\n⚠️ **Network Timeout**: The AI took too long to respond. Please try asking your question again."
            full_response += error_msg
            yield error_msg
        except Exception as e:
            logger.error(f"Unexpected error during chat stream: {e}")
            error_msg = "\n\n⚠️ **Service Disconnected**: The AI service encountered an unexpected error. Please try again."
            full_response += error_msg
            yield error_msg
        
        # 5. Append new messages to our raw history for saving
        raw_history.append({"role": "user", "parts": [message]})
        raw_history.append({"role": "model", "parts": [full_response]})
        
        # 6. Save back to Redis
        await RedisMemoryService.save_history(session_id, raw_history)
