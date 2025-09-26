import logging
from typing import Iterable, Optional, Protocol
from uuid import uuid4

from app.core.config import Settings
from app.schemas.chat import ChatResponse, Message
from app.services.chain.langchain_chat import LangChainChat
from app.services.llm.base import BaseLLMClient

logger = logging.getLogger(__name__)


class ChatMemoryProtocol(Protocol):
    def get_history(self, session_id: str) -> list[Message]:
        ...

    def append_messages(self, session_id: str, messages: list[Message]) -> list[Message]:
        ...

    def set_history(self, session_id: str, messages: list[Message]) -> list[Message]:
        ...


class ChatServiceError(Exception):
    pass


class ChatService:
    def __init__(
        self,
        llm_client: BaseLLMClient,
        memory_backend: ChatMemoryProtocol,
        settings: Settings,
    ) -> None:
        self.llm_client = llm_client
        self.memory_backend = memory_backend
        self.settings = settings
        self.chain = LangChainChat(llm_client)

    async def generate_reply(
        self,
        session_id: Optional[str],
        messages: Iterable[Message],
        context: Optional[dict] = None,
    ) -> ChatResponse:
        messages = list(messages)
        if not messages:
            raise ChatServiceError("Chat request requires at least one message")

        latest_message = messages[-1]
        if latest_message.role != "user":
            raise ChatServiceError("Last message must be sent by the user")

        if session_id is None:
            session_id = str(uuid4())
            logger.debug("Generated new session id %s", session_id)

        history = self.memory_backend.get_history(session_id)
        logger.debug("Existing history length for %s: %s", session_id, len(history))

        prompt_history = history + messages[:-1]
        llm_result = await self.chain.arun(
            history=prompt_history,
            latest_user_message=latest_message.content,
            context=context,
        )

        reply_message = Message(role="assistant", content=llm_result.content)
        updated_history = history + messages + [reply_message]

        if hasattr(self.memory_backend, "set_history"):
            self.memory_backend.set_history(session_id, updated_history)
        else:  # pragma: no cover - defensive fallback
            self.memory_backend.append_messages(session_id, messages + [reply_message])

        logger.debug("Updated history length for %s: %s", session_id, len(updated_history))

        return ChatResponse(session_id=session_id, reply=reply_message, history=updated_history)
