"""Groq LLM API wrapper — plain-language risk explanations."""

from __future__ import annotations

import os

from config import GROQ_API_KEY, GROQ_MODEL


def generate_summary(prompt: str) -> str:
    """Generate a plain-language summary using Groq (Llama 3).

    Returns the LLM text, or a fallback string if the API is unavailable.
    """
    api_key = GROQ_API_KEY or os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return (
            "AI analysis unavailable: No Groq API key configured. "
            "Add GROQ_API_KEY to your environment to enable AI explanations."
        )
    try:
        from groq import Groq

        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as exc:
        return f"AI analysis unavailable: {exc}"
