from __future__ import annotations

from IPython.display import display

from minichat.model.chat_session import ChatSession
from minichat.model.backend_factory import BackendFactory
from minichat.controller.chat_controller import ChatController
from minichat.ui.widgets_view import WidgetsView


class ChatApp:
    """High-level entry point for initializing and displaying the chat UI.

    Responsibilities:
        • Create and wire up the model (ChatSession), controller, and view.
        • Instantiate the selected backend via BackendFactory.
        • Expose a ready-to-display `view` for Jupyter or Colab.

    Example:
        >>> app = ChatApp("echo")
        >>> display(app.view.root)
    """

    def __init__(self, backend_name: str = "echo") -> None:
        """Initialize the chat application.

        Args:
            backend_name: Name of the backend model to use.
        """
        session = ChatSession()
        backend = BackendFactory.create(backend_name)
        controller = ChatController(session, backend)
        self.view = WidgetsView(session, controller)

    def show(self) -> None:
        """Display the chat interface in Jupyter or Colab."""
        display(self.view.root)
