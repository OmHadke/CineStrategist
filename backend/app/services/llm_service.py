"""
LLM Integration Service using the official google-genai SDK.
Handles prompt construction, JSON formatting, structured reasoning,
and seamless fallback to intelligent heuristic synthesis if no API key is supplied.
"""

import os
import json
from typing import Optional, Dict, Any
from app.config import settings

class LLMService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[LLMService] Failed to initialize Google GenAI Client: {e}")

    def is_available(self) -> bool:
        return self.client is not None

    async def generate_json(self, prompt: str, system_instruction: str) -> Optional[Dict[str, Any]]:
        """
        Invokes Gemini with structured JSON output.
        """
        if not self.is_available():
            return None

        try:
            from google.genai import types
            response = self.client.models.generate_content(
                model='gemini-3.8-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    temperature=0.2,
                )
            )
            if response and response.text:
                return json.loads(response.text)
        except Exception as e:
            print(f"[LLMService] Generation error: {e}. Falling back to structured heuristic.")
            return None

llm_service = LLMService()
