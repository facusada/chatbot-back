from typing import Any

from .base import BaseLLMClient, LLMResult


class AnthropicClient(BaseLLMClient):
    provider_name = "anthropic"

    def __init__(self, api_key: str, model: str = "claude-3-haiku-20240307", temperature: float = 0.2):
        if not api_key:
            raise ValueError("Anthropic API key is required")

        try:
            from langchain_anthropic import ChatAnthropic
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise RuntimeError("langchain-anthropic package is missing") from exc

        self._client = ChatAnthropic(
            api_key=api_key,
            model=model,
            temperature=temperature,
        )

    def generate(self, prompt: str, **kwargs: Any) -> LLMResult:
        response = self._client.invoke(prompt)
        content = getattr(response, "content", str(response))
        return LLMResult(content=content, metadata={"provider": self.provider_name})
