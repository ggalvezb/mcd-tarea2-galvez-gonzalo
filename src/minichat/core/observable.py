from __future__ import annotations

from typing import Any, Callable, Dict, List
import logging

logger = logging.getLogger(__name__)


class Observable:
    """Base class for objects that can emit named events with payloads.

    Observers can subscribe to receive notifications in the form
    (event_name, payload). This pattern supports decoupling between
    data models and views or controllers.

    Example:
        def listener(event: str, data: dict[str, Any]) -> None:
            print(f"{event}: {data}")

        subject = Observable()
        subject.subscribe(listener)
        subject._notify("updated", {"count": 10})
    """

    def __init__(self) -> None:
        """Initialize the observer list."""
        self._observers: list[Callable[[str, dict[str, Any]], None]] = []

    def subscribe(self, fn: Callable[[str, dict[str, Any]], None]) -> None:
        """Attach an observer function.

        Args:
            fn: Callback that receives (event_name, payload).

        The same function will not be added twice.
        """
        if fn not in self._observers:
            self._observers.append(fn)

    def unsubscribe(self, fn: Callable[[str, dict[str, Any]], None]) -> None:
        """Detach an observer if it is currently subscribed."""
        if fn in self._observers:
            self._observers.remove(fn)

    def _notify(self, event: str, payload: dict[str, Any] | None = None) -> None:
        """Notify all observers of an event.

        Args:
            event: Name of the event being emitted.
            payload: Optional dictionary of event data.

        Notes:
            Observer errors are caught and logged to prevent propagation.
        """
        data = payload or {}
        for fn in list(self._observers):
            try:
                fn(event, data)
            except Exception as exc:
                logger.debug("Observer %r failed on event %r: %s", fn, event, exc)
