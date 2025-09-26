import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.api.deps import get_chat_service
from app.core.config import Settings
from app.main import create_app
from app.memory.in_memory import InMemoryChatStore
from app.services.chat_service import ChatService
from app.services.llm.base import StubLLMClient


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    return Settings(llm_provider="stub", memory_backend="in_memory", debug=True)


@pytest.fixture()
def chat_service(test_settings: Settings) -> ChatService:
    return ChatService(
        llm_client=StubLLMClient(),
        memory_backend=InMemoryChatStore(),
        settings=test_settings,
    )


@pytest.fixture()
def test_app(chat_service: ChatService):
    app = create_app()
    app.dependency_overrides[get_chat_service] = lambda: chat_service
    yield app
    app.dependency_overrides.clear()


@pytest_asyncio.fixture()
async def async_client(test_app) -> AsyncClient:
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
