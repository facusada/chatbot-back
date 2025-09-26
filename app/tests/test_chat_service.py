import pytest

from app.core.config import Settings
from app.memory.in_memory import InMemoryChatStore
from app.schemas.chat import Message
from app.services.chat_service import ChatService, ChatServiceError
from app.services.llm.base import StubLLMClient


@pytest.fixture()
def service() -> ChatService:
    settings = Settings(llm_provider="stub", memory_backend="in_memory")
    return ChatService(StubLLMClient(), InMemoryChatStore(), settings)


@pytest.mark.asyncio
async def test_generate_reply_creates_session(service: ChatService):
    response = await service.generate_reply(
        session_id=None,
        messages=[Message(role="user", content="Hola, bot")],
        context=None,
    )

    assert response.session_id
    assert response.reply.role == "assistant"
    assert response.history[-1].role == "assistant"
    assert len(response.history) == 2


@pytest.mark.asyncio
async def test_generate_reply_persists_history(service: ChatService):
    first = await service.generate_reply(None, [Message(role="user", content="Hola")])

    second = await service.generate_reply(
        first.session_id,
        [Message(role="user", content="¿Y ahora?")],
    )

    assert second.session_id == first.session_id
    assert len(second.history) == 4


@pytest.mark.asyncio
async def test_generate_reply_validates_last_message_role(service: ChatService):
    with pytest.raises(ChatServiceError):
        await service.generate_reply(
            session_id="session-1",
            messages=[Message(role="assistant", content="Respuesta previa")],
        )
