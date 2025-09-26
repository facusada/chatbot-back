from copy import deepcopy
from threading import Lock
from typing import Dict, List

from app.schemas.chat import Message


class InMemoryChatStore:
    """Simple thread-safe in-memory conversation store keyed by `session_id`."""

    def __init__(self) -> None:
        self._store: Dict[str, List[Message]] = {}
        self._lock = Lock()

    def get_history(self, session_id: str) -> list[Message]:
        with self._lock:
            history = self._store.get(session_id, [])
            return deepcopy(history)

    def append_messages(self, session_id: str, messages: list[Message]) -> list[Message]:
        with self._lock:
            history = self._store.setdefault(session_id, [])
            history.extend(deepcopy(messages))
            return deepcopy(history)

    def set_history(self, session_id: str, messages: list[Message]) -> list[Message]:
        with self._lock:
            self._store[session_id] = deepcopy(messages)
            return deepcopy(self._store[session_id])

    def clear(self, session_id: str) -> None:
        with self._lock:
            self._store.pop(session_id, None)
