"""
llm_client.py

Generic LLM client to support multiple providers (Groq, OpenAI, Google Gemini, Anthropic).
"""

import os

def call_llm(prompt: str, ai_provider: str = "groq", api_key: str = None, temperature: float = 0.4, max_tokens: int = 700) -> str:
    """
    Sends a single-turn prompt to the selected LLM provider and returns the text response.
    """
    if not api_key:
        if ai_provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
        elif ai_provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
        elif ai_provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
        elif ai_provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
        elif ai_provider == "openrouter":
            api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError(f"API key is not provided for {ai_provider}. Please enter a valid API key in the form.")

    try:
        if ai_provider == "groq":
            from groq import Groq
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()

        elif ai_provider == "openai":
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()

        elif ai_provider == "gemini":
            from google import genai
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt,
                config={"temperature": temperature, "max_output_tokens": max_tokens},
            )
            return response.text.strip()

        elif ai_provider == "anthropic":
            from anthropic import Anthropic
            client = Anthropic(api_key=api_key)
            response = client.messages.create(
                model="claude-3-5-sonnet-latest",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.content[0].text.strip()

        elif ai_provider == "openrouter":
            from openai import OpenAI
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )
            response = client.chat.completions.create(
                model="meta-llama/llama-3.3-70b-instruct",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()

        else:
            raise RuntimeError(f"Unknown AI Provider: {ai_provider}")

    except Exception as exc:
        raise RuntimeError(f"{ai_provider.capitalize()} API request failed: {exc}") from exc
