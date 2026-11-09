from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class GenerationConfig:
    """Immutable configuration for text generation parameters.

    Attributes:
        temperature: Sampling temperature; higher values produce
            more random output (default: 0.7).
        top_p: Nucleus sampling probability threshold (default: 0.95).
        top_k: Limit of highest-probability tokens to consider (default: 50).
        max_new_tokens: Maximum number of tokens to generate (default: 120).
        max_ctx_tokens: Maximum context length to retain (default: 900).

    Example:
        cfg = GenerationConfig(temperature=0.8, top_p=0.9)
    """

    temperature: float = 0.7
    top_p: float = 0.95
    top_k: int = 50
    max_new_tokens: int = 120
    max_ctx_tokens: int = 900
