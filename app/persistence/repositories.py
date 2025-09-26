from typing import Iterable, Sequence

from sqlalchemy.orm import Session

from app.persistence.models import ChatMessage
from app.schemas.chat import Message


class ChatHistoryRepository:
    """Repository for persisting chat messages using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session = session

    def save_messages(self, session_id: str, messages: Iterable[Message]) -> None:
        for message in messages:
            db_message = ChatMessage(
                session_id=session_id,
                role=message.role,
                content=message.content,
            )
            self.session.add(db_message)

    def get_history(self, session_id: str) -> Sequence[ChatMessage]:
        return (
            self.session.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.asc())
            .all()
        )
