import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import partial
from typing import Any, Dict


@dataclass
class LLMResult:
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseLLMClient(ABC):
    provider_name: str = "base"

    @abstractmethod
    def generate(self, prompt: str, **kwargs: Any) -> LLMResult:
        raise NotImplementedError

    async def agenerate(self, prompt: str, **kwargs: Any) -> LLMResult:
        loop = asyncio.get_running_loop()
        func = partial(self.generate, prompt, **kwargs)
        return await loop.run_in_executor(None, func)


class StubLLMClient(BaseLLMClient):
    provider_name = "stub"

    def generate(self, prompt: str, **kwargs: Any) -> LLMResult:
        content = "Stub response: " + prompt.splitlines()[-1].strip()
        return LLMResult(content=content, metadata={"provider": self.provider_name})
