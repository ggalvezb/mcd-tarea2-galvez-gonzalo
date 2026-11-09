from __future__ import annotations

from typing import Any, Optional

from minichat.model.message import Message
from minichat.model.role import Role
from minichat.core.observable import Observable


class ChatSession(Observable):
    """Observable model that stores the sequence of chat messages.

    Responsibilities:
        • Maintain message history (add, delete, clear)
        • Notify observers when the message list changes
        • Provide read-only views of stored messages

    Emits events:
        - "messages_updated": fired after any modification.
    """

    def __init__(self) -> None:
        """Initialize an empty session."""
        super().__init__()
        self._messages: list[Message] = []

    def add(
        self,
        role: Role,
        content: str,
        meta: Optional[dict[str, Any]] = None,
    ) -> None:
        """Add a new message to the conversation."""
        self._messages.append(
            Message(role=role, content=content, meta=meta or {})
        )
        self._notify("messages_updated", {})

    def delete_at(self, index: int) -> None:
        """Delete a message by its index if it exists."""
        if 0 <= index < len(self._messages):
            del self._messages[index]
            self._notify("messages_updated", {})

    def clear(self) -> None:
        """Remove all messages from the session."""
        self._messages.clear()
        self._notify("messages_updated", {})

    def all(self) -> list[Message]:
        """Return a shallow copy of the message list."""
        return list(self._messages)

    def as_public(self) -> list[dict[str, Any]]:
        """Return a JSON-serializable representation of the chat history."""
        return [
            {
                "role": m.role.value,
                "content": m.content,
                "timestamp": m.timestamp.isoformat(),
                "meta": m.meta,
            }
            for m in self._messages
        ]

    def get_summary(self) -> list[dict[str, Any]]:
        """Return a serializable representation of the chat history."""
        result = []
        for m in self._messages:
            result.append({
                "role": m.role.value,
                "content": m.content,
                "timestamp": m.timestamp.isoformat(),
                "meta": m.meta,
            })
        return result

    def get_observer_count(self) -> int:
        """Return the number of subscribed observers."""
        return len(self._observers)

    def has_observers(self) -> bool:
        """Check if there are any subscribed observers."""
        return len(self._observers) > 0
