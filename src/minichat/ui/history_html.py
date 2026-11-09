from __future__ import annotations

import json
from typing import Any, Dict, List

from minichat.model.message import Message
from minichat.model.role import Role


class HistoryHTML:
    """Render chat history as formatted HTML for display in notebooks.

    Responsibilities:
        • Convert a list of Message objects into styled HTML.
        • Escape user text to prevent HTML injection.
        • Color-code messages by sender role.

    Example:
        html = HistoryHTML()
        display(HTML(html.render(session.all())))
    """

    _COLORS: dict[Role, str] = {
        Role.USER: "#1a73e8",
        Role.ASSISTANT: "#188038",
        Role.SYSTEM: "#5f6368",
    }

    def render(self, messages: list[Message]) -> str:
        """Render the entire chat history as HTML.

        Args:
            messages: List of Message instances to render.

        Returns:
            A string containing HTML markup for display.
        """
        parts: list[str] = ["<b>Conversation</b>"]
        for message in messages:
            parts.append(self._item(message))

        # Add a bottom marker for automatic scroll
        parts.extend(
            [
                "<div id='bm' style='height:1px;'></div>",
                "<script>document.getElementById('bm').scrollIntoView();</script>",
            ]
        )
        return "\n".join(parts)

    def _item(self, message: Message) -> str:
        """Render a single message block as HTML."""
        color = self._COLORS.get(message.role, "#5f6368")
        timestamp = message.timestamp.strftime("%H:%M:%S")
        text = self._escape(message.content)
        meta_html = self._format_meta(message.meta)

        return (
            f"<div style='margin:6px 0;'>"
            f"<span style='color:{color};font-weight:600'>"
            f"{message.role.value.upper()}</span>"
            f"<span style='color:#999;font-size:12px;margin-left:6px;'>"
            f"{timestamp}</span><br/>"
            f"<div style='white-space:pre-wrap;margin-left:8px;'>{text}</div>"
            f"{meta_html}"
            f"</div>"
        )

    def _format_meta(self, meta: dict[str, Any]) -> str:
        """Render metadata below a message, if any."""
        if not meta:
            return ""
        safe_meta = self._escape(json.dumps(meta, ensure_ascii=False))
        return (
            f"<div style='color:#777;font-size:11px;margin-left:8px;'>"
            f"meta: {safe_meta}</div>"
        )

    def _escape(self, text: str) -> str:
        """Escape HTML special characters to prevent injection."""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )
