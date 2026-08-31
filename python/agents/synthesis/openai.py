"""LLM wrapper -- single point of LLM access for all agents.

S: Single responsibility -- sends prompts to LLM, returns text.
D: Agents depend on SynthesizerInterface, not this class directly.
DRY: Every agent calls this. No scattered LLM imports.
"""

import os
from typing import Optional

from openai import OpenAI

from agents.base import SynthesizerInterface

LLM_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
LLM_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-v4-flash"


class OpenAISynthesizer(SynthesizerInterface):
    """Wraps DeepSeek API (OpenAI-compatible).

    Use thinking=True for complex tasks. system message sets behavior.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        thinking: bool = False,
    ):
        self.client = OpenAI(
            api_key=api_key or LLM_API_KEY,
            base_url=LLM_BASE_URL,
        )
        self.model = model
        self.thinking = thinking

    def synthesize(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        system: Optional[str] = None,
    ) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        kwargs = dict(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        if self.thinking:
            kwargs["reasoning_effort"] = "medium"
        if max_tokens:
            kwargs["max_tokens"] = max_tokens

        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content or ""
