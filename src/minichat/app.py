from __future__ import annotations

import sys

from minichat.model.chat_session import ChatSession
from minichat.model.backend_factory import BackendFactory
from minichat.controller.chat_controller import ChatController
from minichat.model.role import Role


def _last_assistant_text(session: ChatSession) -> str | None:
    """Return the content of the most recent assistant message, if any."""
    for m in reversed(session.all()):
        if m.role == Role.ASSISTANT:
            return m.content
    return None


def main(backend_name: str = "echo") -> None:
    session = ChatSession()
    backend = BackendFactory.create(backend_name)
    controller = ChatController(session, backend)

    print(f"MiniChat console [{backend.name}] — type 'exit' to quit.")
    while True:
        msg = input("You: ").strip()
        if not msg:
            continue
        if msg.lower() in {"exit", "quit"}:
            break
        try:
            controller.send_user(msg)
        except Exception as e:
            print(f"[backend error] {e}")
            continue
        reply = _last_assistant_text(session) or "(no reply)"
        print("Bot:", reply)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "echo")
