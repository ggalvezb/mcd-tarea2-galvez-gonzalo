from __future__ import annotations

from typing import Optional

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from minichat.model.chat_session import ChatSession
from minichat.model.generation_config import GenerationConfig
from minichat.model.role import Role


class DialoGPTBackend:
    """Thin wrapper around a DialoGPT model for conversational replies.

    Responsibilities:
        • Keep tokenizer/model loaded on the chosen device
        • Build context from a ChatSession
        • Generate a single assistant reply with sampling

    Notes:
        This backend is intentionally minimal: no streaming,
        no memory beyond the given session, and no persistence.
    """

    def __init__(self, model_name: str = "microsoft/DialoGPT-medium") -> None:
        """Load tokenizer and model on CPU/GPU; set basic generation defaults.

        Args:
            model_name: Hugging Face model identifier.

        Raises:
            OSError: If the model or tokenizer cannot be downloaded/loaded.
        """
        device_str = "cuda" if torch.cuda.is_available() else "cpu"
        self._device = torch.device(device_str)

        self._tok = AutoTokenizer.from_pretrained(model_name)
        self._model = (
            AutoModelForCausalLM.from_pretrained(model_name)
            .to(self._device)
            .eval()
        )

        # Prefer the provided name; fallback to tokenizer's name for display.
        self._name = model_name or getattr(self._tok, "name_or_path", "DialoGPT")

        # Ensure special tokens are valid for generation.
        self._ensure_special_tokens()

    # --------------------------------------------------------------------- #
    # Internals
    # --------------------------------------------------------------------- #

    def _ensure_special_tokens(self) -> None:
        """Ensure pad/eos tokens are valid for generation.

        Many DialoGPT checkpoints lack an explicit pad token. We default
        pad to eos, which is acceptable for causal decoding. We also
        update the model config so `.generate()` uses consistent IDs.
        """
        if self._tok.pad_token_id is None:
            # Reuse eos as pad for left-unpadded, causal decoding scenarios.
            self._tok.pad_token = self._tok.eos_token

        # Make sure model config sees them too.
        self._model.config.pad_token_id = self._tok.pad_token_id
        self._model.config.eos_token_id = self._tok.eos_token_id

    def _encode_turn(self, text: str) -> torch.Tensor:
        """Encode a single utterance terminated by eos."""
        # shape: (1, seq_len)
        ids = self._tok.encode(
            text + (self._tok.eos_token or ""),
            return_tensors="pt",
        )
        return ids.to(self._device)
    
    def _encode_system_message(self, text: str) -> torch.Tensor:
        """Encode a system message with the [SYS] prefix."""
        system_text = f"[SYS] {text}"
        encoded = self._tok.encode(
            system_text + (self._tok.eos_token or ""),
            return_tensors="pt",
        )
        return encoded.to(self._device)

    def _build_ctx(self, session: ChatSession, max_ctx: int) -> torch.Tensor:
        """Concatenate all turns into a single input, clipped to max_ctx.

        Args:
            session: Conversation state.
            max_ctx: Maximum context length (in tokens) to keep.

        Returns:
            A tensor of shape (1, ctx_len) on the backend device.
        """
        ids: Optional[torch.Tensor] = None

        for m in session.all():
            txt = m.content if m.role != Role.SYSTEM else f"[SYS] {m.content}"
            turn = self._encode_turn(txt)
            ids = turn if ids is None else torch.cat([ids, turn], dim=-1)

        if ids is None:
            ids = self._encode_turn("Hello!")

        # Trim right side to respect context budget.
        if ids.shape[-1] > max_ctx:
            ids = ids[:, -max_ctx:]

        return ids

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #

    @torch.no_grad()
    def reply(self, session: ChatSession, cfg: GenerationConfig) -> str:
        """Generate a single reply given the current session and config.

        Args:
            session: Conversation state.
            cfg: Generation parameters (temperature, top_p, etc.).

        Returns:
            The assistant's reply (never empty; falls back to '(no reply)').
        """
        ctx = self._build_ctx(session, cfg.max_ctx_tokens)

        # Attention mask prevents HF warning when pad == eos, and is the
        # reliable way to inform generation which tokens are valid.
        attention_mask = torch.ones_like(
            ctx, dtype=torch.long, device=self._device
        )

        out = self._model.generate(
            ctx,
            attention_mask=attention_mask,
            max_new_tokens=cfg.max_new_tokens,
            do_sample=True,
            temperature=cfg.temperature,
            top_p=cfg.top_p,
            top_k=cfg.top_k,
            pad_token_id=self._tok.pad_token_id,
            eos_token_id=self._tok.eos_token_id,
        )

        # New tokens are everything generated after the context length.
        new_tokens = out[:, ctx.shape[-1]:][0]
        text = self._tok.decode(new_tokens, skip_special_tokens=True).strip()
        return text or "(no reply)"

    @property
    def name(self) -> str:
        """Display name of the backend/model."""
        return self._name
