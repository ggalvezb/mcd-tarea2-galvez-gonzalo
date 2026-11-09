from __future__ import annotations
from enum import Enum


class Role(str, Enum):
    """Enumeration of the message sender roles.

    Values:
        SYSTEM: Represents messages produced by the system or framework.
        USER: Represents user input messages.
        ASSISTANT: Represents assistant or model responses.

    Example:
        role = Role.USER
        print(role.value)  # "user"
    """

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

    @classmethod
    def list(cls) -> list[str]:
        """Return all available role string values."""
        return [r.value for r in cls]
