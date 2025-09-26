from fastapi import Depends

from app.core.config import Settings, get_settings
from app.memory.in_memory import InMemoryChatStore
from app.memory.sqlite_memory import SQLiteChatMemory
from app.services.chat_service import ChatService
from app.services.llm.anthropic_client import AnthropicClient
from app.services.llm.base import BaseLLMClient, StubLLMClient
from app.services.llm.local_llama import LocalLlamaClient
from app.services.llm.openai_client import OpenAIClient


_in_memory_store = InMemoryChatStore()


def get_llm_client(settings: Settings) -> BaseLLMClient:
    provider = settings.llm_provider

    if provider == "openai" and settings.openai_api_key:
        return OpenAIClient(api_key=settings.openai_api_key)
    if provider == "anthropic" and settings.anthropic_api_key:
        return AnthropicClient(api_key=settings.anthropic_api_key)
    if provider == "local":
        return LocalLlamaClient()
    return StubLLMClient()


def get_memory_backend(settings: Settings):
    if settings.memory_backend == "sqlite":
        return SQLiteChatMemory(settings.database_url)
    return _in_memory_store


def get_chat_service(settings: Settings = Depends(get_settings)) -> ChatService:
    llm_client = get_llm_client(settings)
    memory_backend = get_memory_backend(settings)
    return ChatService(llm_client=llm_client, memory_backend=memory_backend, settings=settings)
