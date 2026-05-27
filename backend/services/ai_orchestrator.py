import os
import json
import google.generativeai as genai
from typing import Dict, Any, Type
from pydantic import BaseModel
from utils.logger import logger
from prompts.system.core import SYSTEM_PROMPT

# Configure Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY:
    genai.configure(api_key=GROQ_API_KEY)
else:
    logger.warning("GROQ_API_KEY is not set. AI Orchestrator will fail.")

# Configure Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY:
    genai.configure(api_key=GROQ_API_KEY)
else:
    logger.warning("GROQ_API_KEY is not set. AI Orchestrator will fail.")

class AIOrchestrator:
    """
    Service responsible for communicating with Groq.
    """

    def __init__(self, model_name: str = "llama-3.1-8b-instant"):
        self.model_name = model_name

    def _get_model(self, temperature: float = 1.0) -> genai.GenerativeModel:
        """
        Initialize the generative model for structured output using plain JSON generation.
        """
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            response_mime_type="application/json"
        )

        return genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=SYSTEM_PROMPT,
            generation_config=generation_config
        )

    async def extract_structured_data(self, prompt: str, schema: Type[BaseModel]) -> BaseModel:
        """
        Extract structured data using Gemini based on a Pydantic schema with automatic retries.
        """
        import time
        import asyncio
        from pydantic import ValidationError
        from services.response_sanitizer import ResponseSanitizer
        
        logger.info(f"Calling Groq ({self.model_name}) for structured data extraction.")
        
        max_retries = 2
        attempt = 0
        temperatures = [1.0, 0.4, 0.1] # Decrease temperature on retries for more deterministic output
        
        while attempt <= max_retries:
            start_time = time.time()
            current_temp = temperatures[attempt]
            
            try:
                model = self._get_model(temperature=current_temp)
                # Enforce a 20-second timeout to prevent indefinite hangs
                response = await asyncio.wait_for(
                    model.generate_content_async(prompt), 
                    timeout=90.0
                )
                
                latency = time.time() - start_time
                
                # Extract token usage if available
                usage = response.usage_metadata
                if usage:
                    logger.info(f"AI Usage (Attempt {attempt+1}) - Prompt Tokens: {usage.prompt_token_count}, "
                                f"Candidate Tokens: {usage.candidates_token_count}, "
                                f"Total: {usage.total_token_count}, Latency: {latency:.2f}s")
                
                # Sanitize the raw JSON string before validation
                raw_json = response.text
                logger.debug(f"DEBUG - Raw Gemini Response: {raw_json[:150]}...")
                
                sanitized_json = ResponseSanitizer.sanitize(raw_json)
                
                # Parse the JSON response into the Pydantic model
                parsed_data = schema.model_validate_json(sanitized_json)
                return parsed_data
                
            except (json.JSONDecodeError, ValidationError) as e:
                logger.warning(f"Validation or Parse error on attempt {attempt+1}: {str(e)}")
                attempt += 1
                if attempt > max_retries:
                    logger.error("Max retries reached. AI extraction failed.")
                    raise ValueError(f"Failed to generate valid structured data after {max_retries+1} attempts.")
            except Exception as e:
                logger.error(f"Unexpected error during Gemini extraction on attempt {attempt+1}: {e}")
                raise
