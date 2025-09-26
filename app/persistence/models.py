from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.persistence.db import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: int = Column(Integer, primary_key=True, index=True)
    session_id: str = Column(String(255), index=True, nullable=False)
    role: str = Column(String(32), nullable=False)
    content: str = Column(Text, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:  # pragma: no cover - repr helper
        return f"<ChatMessage session={self.session_id} role={self.role}>"
