from __future__ import annotations

import random

from minichat.model.generation_config import GenerationConfig
from minichat.model.role import Role


class EchoBackend:
    """Lightweight backend that needs no model download.

    It answers with a canned sentence built from the last user message,
    so the whole application can be exercised on any laptop without
    torch/transformers. Use it for manual testing while refactoring.
    """

    _TEMPLATES = [
        "You said: \"{text}\". Tell me more.",
        "Interesting. Why do you think \"{text}\"?",
        "I see. \"{text}\" is a good point.",
    ]

    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)

    def reply(self, session, cfg: GenerationConfig) -> str:
        last_user = ""
        for m in reversed(session.all()):
            if m.role == Role.USER:
                last_user = m.content
                break
        template = self._rng.choice(self._TEMPLATES)
        text = template.format(text=last_user[: cfg.max_new_tokens])
        return text or "(no reply)"

    @property
    def name(self) -> str:
        return "echo"
