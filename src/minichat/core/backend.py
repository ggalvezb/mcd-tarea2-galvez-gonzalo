from __future__ import annotations

from typing import Protocol, runtime_checkable

from minichat.model.generation_config import GenerationConfig


@runtime_checkable
class Backend(Protocol):
    """Interface that every text-generation backend must implement."""

    @property
    def name(self) -> str:
        """Display name of the backend."""
        ...

    def reply(self, session, cfg: GenerationConfig) -> str:
        """Generate one assistant reply for the given session."""
        ...
