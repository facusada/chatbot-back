from datetime import UTC, datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


RoleLiteral = Literal["system", "user", "assistant"]


class Message(BaseModel):
    role: RoleLiteral
    content: str = Field(..., min_length=1)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(default=None, description="Conversation identifier")
    messages: list[Message]
    context: Optional[dict] = Field(default=None, description="Optional metadata passed to the chain")


class ChatResponse(BaseModel):
    session_id: str
    reply: Message
    history: list[Message]
