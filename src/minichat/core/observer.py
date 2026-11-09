from __future__ import annotations

from typing import Any, Dict


class Observer:
    """Base class for objects that react to events emitted by observables.

    Subclasses must override :meth:`on_event` to handle notifications
    from an Observable.

    Example:
        class PrintObserver(Observer):
            def on_event(self, event: str, payload: dict[str, Any]) -> None:
                print(f"Received {event}: {payload}")

        obs = PrintObserver()
        obs.on_event("data_changed", {"count": 42})
    """

    def on_event(self, event: str, payload: dict[str, Any]) -> None:
        """Handle an event emitted by an observable.

        Args:
            event: The event name.
            payload: A dictionary containing event-specific data.

        Raises:
            NotImplementedError: If the subclass does not override this method.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__}.on_event() must be implemented"
        )
