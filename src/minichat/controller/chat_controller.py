from __future__ import annotations

import json
import logging
import time
from dataclasses import asdict
from typing import Any, Optional

from minichat.core.backend import Backend
from minichat.core.observable import Observable
from minichat.model.chat_session import ChatSession
from minichat.model.generation_config import GenerationConfig
from minichat.model.role import Role

logger = logging.getLogger(__name__)


class ChatController(Observable):
    """Coordinates the conversation between session and backend.

    Emits the following observable events:
        - "config_changed": after updating GenerationConfig
        - "generating_start": before calling the backend
        - "generating_done": after a reply (payload: {"reply": str})
        - "generating_error": on backend exception
          (payload: {"error": str})
        - "messages_updated": after session mutations
        - "export_done": after exporting JSON (payload: {"path": str})
    """

    def __init__(
        self,
        session: ChatSession,
        backend: Backend,
        *,
        logger_: Optional[logging.Logger] = None,
    ) -> None:
        """Initialize with dependencies and default config.

        Note:
            Dependencies are injected to ease testing with fakes/mocks.
        """
        super().__init__()
        self._session = session
        self._backend = backend
        self._cfg = GenerationConfig()
        self._log = logger_ or logger

    @property
    def session(self) -> ChatSession:
        """Read-only access to the session."""
        return self._session

    @property
    def backend(self) -> Backend:
        """Read-only access to the backend."""
        return self._backend

    @property
    def config(self) -> GenerationConfig:
        """Current generation configuration."""
        return self._cfg

    def set_generation(
        self,
        temperature: float,
        top_p: float,
        top_k: int,
        max_new_tokens: int,
        max_ctx_tokens: int,
    ) -> None:
        """Update generation parameters.

        Raises:
            ValueError: If any value is invalid.
        """
        if temperature <= 0:
            raise ValueError("temperature must be positive")
        if not (0 < top_p <= 1):
            raise ValueError("top_p must be in (0, 1]")
        if top_k < 0:
            raise ValueError("top_k must be >= 0")
        if max_new_tokens <= 0:
            raise ValueError("max_new_tokens must be positive")
        if max_ctx_tokens <= 0:
            raise ValueError("max_ctx_tokens must be positive")

        self._cfg = GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_new_tokens=max_new_tokens,
            max_ctx_tokens=max_ctx_tokens,
        )
        self._notify("config_changed", {"cfg": asdict(self._cfg)})

    def send_user(self, text: str) -> None:
        """Append a user message, ask the backend for a reply and store it.

        Emits:
            generating_start -> generating_done | generating_error
            messages_updated on session mutations.

        Raises:
            ValueError: If text is empty or whitespace.
        """
        # 1. Validate input
        if text is None:
            text = ""
        text = text.strip()
        if len(text) == 0:
            raise ValueError("text cannot be empty")
        if len(text) > 2000:
            text = text[:2000]

        # 2. Store the user turn
        self._session.add(Role.USER, text)
        self._notify("generating_start", {})

        # 3. Call the backend and measure latency
        started = time.perf_counter()
        try:
            reply = self._backend.reply(self._session, self._cfg)
        except Exception as exc:
            self._log.exception("Backend error during reply")
            self._notify("generating_error", {"error": str(exc)})
            return
        elapsed_ms = int((time.perf_counter() - started) * 1000)

        # 4. Build metadata for the assistant turn
        meta: dict[str, Any] = {
            "backend": self._backend.name,
            "gen_cfg": asdict(self._cfg),
            "latency_ms": elapsed_ms,
            "prompt_chars": len(text),
            "reply_chars": len(reply),
        }
        self._log.debug("reply generated in %d ms", elapsed_ms)

        # 5. Store the assistant turn
        self._session.add(Role.ASSISTANT, reply, meta=meta)
        self._notify("generating_done", {"reply": reply})

    def add_assistant(self, text: str) -> None:
        """Manually append an assistant message (no generation)."""
        text = self._validate_text(text)
        if not text:
            return
        self._session.add(Role.ASSISTANT, text)
        self._notify("messages_updated", {})

    def add_system(self, text: str) -> None:
        """Append a system message."""
        text = self._validate_text(text)
        if not text:
            return
        self._session.add(Role.SYSTEM, text)
        self._notify("messages_updated", {})

    def delete_at(self, index: int) -> None:
        """Delete the message at the given index."""
        self._session.delete_at(index)
        self._notify("messages_updated", {})

    def clear_all(self) -> None:
        """Remove every message from the session."""
        self._session.clear()
        self._notify("messages_updated", {})

    def get_observer_count(self) -> int:
        """Return the number of subscribed observers."""
        return len(self._observers)

    def has_observers(self) -> bool:
        """Check if there are any subscribed observers."""
        return len(self._observers) > 0

    def export_json(self, path: str = "chat_transcript.json") -> None:
        """Export the conversation transcript as JSON."""
        data = self._session.get_summary()
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        self._notify("export_done", {"path": path})

    def _validate_text(self, text: Optional[str]) -> str:
        """Return the stripped text, or '' when it is None/blank."""
        return (text or "").strip()
