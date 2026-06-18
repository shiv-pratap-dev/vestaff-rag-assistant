"""
LLM utilities.

Handles communication with the Hugging Face Router
and returns generated responses.
"""

import requests

from app.core.config import settings


class HFLLM:
    """
    Wrapper for Hugging Face Router (OpenAI-compatible)
    Chat Completions API
    """

    def __init__(self, timeout: int = 60):

        self.base_url = settings.HF_API_BASE_URL.rstrip("/")
        self.model = settings.LLM_MODEL
        self.token = settings.HF_TOKEN
        self.timeout = timeout

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        self.chat_url = f"{self.base_url}/chat/completions"

    def invoke(
        self,
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.0
    ) -> str:
        """
        Sends a prompt to the configured LLM and
        returns the generated answer.
        """

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an AI assistant specialized in answering "
                        "questions about the AWS Customer Agreement. "
                        "Answer ONLY using the provided document context. "
                        "If the answer is not present in the context, reply "
                        "exactly: "
                        "'I could not find the answer in the provided document.'"
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        try:

            response = requests.post(
                self.chat_url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )

            response.raise_for_status()

        except requests.RequestException as e:
            raise RuntimeError(
                f"Hugging Face request failed: {e}"
            )

        try:
            data = response.json()

            return (
                data["choices"][0]
                ["message"]
                ["content"]
                .strip()
            )

        except Exception:
            raise RuntimeError(
                f"Unable to parse HF response: {data}"
            )


# Singleton instance used across the application
llm = HFLLM()