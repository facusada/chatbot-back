from typing import Any

from .base import BaseLLMClient, LLMResult


class OpenAIClient(BaseLLMClient):
    provider_name = "openai"

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo-0125", temperature: float = 0.2):
        if not api_key:
            raise ValueError("OpenAI API key is required")

        try:
            from langchain_openai import ChatOpenAI
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise RuntimeError("langchain-openai package is missing") from exc

        self._client = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=temperature,
        )

    def generate(self, prompt: str, **kwargs: Any) -> LLMResult:
        response = self._client.invoke(prompt)
        content = getattr(response, "content", str(response))
        return LLMResult(content=content, metadata={"provider": self.provider_name})
