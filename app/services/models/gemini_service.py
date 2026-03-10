from google import genai
from google.genai import types
from app.core.config import settings
from app.services.models.base_llm import BaseLLMService
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class GeminiService(BaseLLMService):
    def __init__(self):
        if settings.GEMINI_API_KEY:
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
            self.model_name = "gemini-1.5-flash"
        else:
            self.client = None
            logger.warning("GEMINI_API_KEY not found. Gemini Service disabled.")

    def health_check(self) -> bool:
        return self.client is not None

    def generate(self, system_prompt: str, user_prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        if not self.client:
            raise ValueError("Gemini Service is not configured.")

        try:
            final_user_prompt = user_prompt
            if context and context.get("history"):
                history_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in context["history"]])
                final_user_prompt = f"Previous Conversation Context:\n{history_text}\n\nUser Question: {user_prompt}"

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=final_user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                )
            )

            if not response.text:
                raise ValueError("Gemini returned an empty response (possibly blocked or safety triggered)")

            return response.text
        except Exception as e:
            logger.error(f"Gemini Generation Error: {e}")
            try:
                combined_prompt = f"{system_prompt}\n\nUSER: {user_prompt}"
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=combined_prompt,
                )
                return response.text
            except Exception as e2:
                logger.error(f"Gemini Hard Failure: {e2}")
                raise e2
