from __future__ import annotations

from minichat.core.backend import Backend
from minichat.model.echo_backend import EchoBackend


class BackendFactory:
    """Factory class for creating backend instances.

    Supported names:
        - "echo": offline backend, no downloads (recommended for testing).
        - "DialoGPT-medium": Hugging Face model (requires torch + transformers).

    Example:
        backend = BackendFactory.create("echo")
        print(backend.name)
    """

    @staticmethod
    def create(name: str = "echo") -> Backend:
        """Return a backend instance based on the given name.

        Raises:
            ValueError: If the backend name is not supported.
        """
        key = name.lower()
        if key == "echo":
            return EchoBackend()
        if key == "dialogpt-medium":
            # Imported lazily so that torch is only required when used.
            from minichat.model.dialogpt_backend import DialoGPTBackend

            return DialoGPTBackend("microsoft/DialoGPT-medium")

        raise ValueError(f"Unsupported backend: {name}")
