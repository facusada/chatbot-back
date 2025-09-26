from typing import Any

from .base import BaseLLMClient, LLMResult


class LocalLlamaClient(BaseLLMClient):
    provider_name = "local"

    def __init__(self, model_path: str | None = None):
        # A real implementation could load transformers/llama.cpp weights here.
        self.model_path = model_path

    def generate(self, prompt: str, **kwargs: Any) -> LLMResult:
        reversed_prompt = " ".join(reversed(prompt.split()))
        content = f"Local model reply (echo): {reversed_prompt}"
        metadata = {"provider": self.provider_name, "model_path": self.model_path}
        return LLMResult(content=content, metadata=metadata)
