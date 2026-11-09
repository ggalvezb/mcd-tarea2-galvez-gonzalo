from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict

from minichat.model.role import Role


@dataclass(frozen=True)
class Message:
    """Immutable chat message entity.

    Attributes:
        role: The sender role (system, user, or assistant).
        content: Text content of the message.
        timestamp: UTC timestamp of message creation.
        meta: Optional metadata (e.g., backend info or parameters).

    Example:
        msg = Message(role=Role.USER, content="Hello!")
        print(msg.summary())
    """

    role: Role
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    meta: dict[str, Any] = field(default_factory=dict)

    def summary(self) -> str:
        """Return a short, human-readable summary for display."""
        hhmm = self.timestamp.strftime("%H:%M:%S")
        text = self.content
        preview = f"{text[:30]}…" if len(text) > 30 else text
        return f"[{hhmm}] {self.role.value}: {preview}"
