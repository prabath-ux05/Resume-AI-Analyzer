import os
import json
import asyncio
import time

from groq import AsyncGroq
from typing import Type
from pydantic import BaseModel, ValidationError

from utils.logger import logger
from prompts.system.core import SYSTEM_PROMPT
from services.response_sanitizer import ResponseSanitizer


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    logger.warning("GROQ_API_KEY is not set. AI Orchestrator will fail.")


class AIOrchestrator:
    """
    Service responsible for communicating with Groq.
    """

    def __init__(self, model_name: str = "llama-3.1-8b-instant"):
        self.model_name = model_name
        self.client = AsyncGroq(api_key=GROQ_API_KEY)

    async def extract_structured_data(
        self,
        prompt: str,
        schema: Type[BaseModel]
    ) -> BaseModel:

        logger.info(f"Calling Groq ({self.model_name})")

        max_retries = 2

        for attempt in range(max_retries + 1):

            start_time = time.time()

            try:

                response = await asyncio.wait_for(
                    self.client.chat.completions.create(
                        model=self.model_name,
                        temperature=0.1,
                        response_format={"type": "json_object"},
                        messages=[
                            {
                                "role": "system",
                                "content": SYSTEM_PROMPT
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    ),
                    timeout=90.0
                )

                latency = time.time() - start_time

                raw_json = response.choices[0].message.content

                logger.info(
                    f"Groq response received in {latency:.2f}s"
                )

                logger.debug(
                    f"RAW RESPONSE: {raw_json[:200]}"
                )

                sanitized_json = ResponseSanitizer.sanitize(raw_json)

                parsed_data = schema.model_validate_json(
                    sanitized_json
                )

                return parsed_data

            except (json.JSONDecodeError, ValidationError) as e:

                logger.warning(
                    f"Validation error attempt {attempt+1}: {e}"
                )

                if attempt == max_retries:
                    raise ValueError(
                        "Failed to generate valid structured data."
                    )

            except asyncio.TimeoutError:

                logger.error("Groq request timeout")

                if attempt == max_retries:
                    raise ValueError(
                        "Groq request timed out."
                    )

            except Exception as e:

                logger.error(f"Unexpected Groq error: {e}")
                raise