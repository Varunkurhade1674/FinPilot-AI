"""
groq_client.py

Small shared helper that wraps the Groq API so every agent calls the
LLM in exactly the same way (same client, same model, same error handling).
"""

import os
from groq import Groq

# Model used for every agent. Llama 3.3 70B Versatile is Groq's
# general-purpose reasoning model - good balance of quality and speed.
MODEL_NAME = "llama-3.3-70b-versatile"


def call_llm(prompt: str, api_key: str = None, temperature: float = 0.4, max_tokens: int = 700) -> str:
    """
    Sends a single-turn prompt to the Groq LLM and returns the text response.

    Raises a RuntimeError with a friendly message if the API key is missing
    or if the request fails, so calling agents can surface a clean error
    to the user instead of crashing.
    """
    key = api_key or os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError(
            "GROQ_API_KEY is not provided. Please enter a valid API key in the form."
        )

    try:
        client = Groq(api_key=key)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:  # noqa: BLE001 - we want to catch any SDK/network error
        raise RuntimeError(f"Groq API request failed: {exc}") from exc
