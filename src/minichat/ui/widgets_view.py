from __future__ import annotations

from typing import Any, List, Tuple

import ipywidgets as widgets
from IPython.display import HTML, clear_output, display

from minichat.core.observer import Observer
from minichat.controller.chat_controller import ChatController
from minichat.model.chat_session import ChatSession
from minichat.model.role import Role
from minichat.ui.history_html import HistoryHTML
from minichat.core.events import Event
from dataclasses import replace

class WidgetsView(Observer):
    """Notebook UI that observes both the session and the controller.

    Responsibilities:
        • Build a simple ipywidgets-based chat interface.
        • React to observable events to update UI state.
        • Delegate all actions to the controller.
    """

    def __init__(self, session: ChatSession, controller: ChatController) -> None:
        self._session = session
        self._ctl = controller
        self._fmt = HistoryHTML()

        self._build_header()
        self._build_output()
        self._build_inputs()
        self._build_params()
        self._build_manage()
        self._compose_layout()
        self._wire_events()

        # Observe both model and controller
        self._session.subscribe(self.on_event)
        self._ctl.subscribe(self.on_event)

        # Initial render
        self._render()

    # ---------- Build sections ----------

    def _build_header(self) -> None:
        self.title = widgets.HTML("<h3>DialoGPT — MVC (observer)</h3>")

    def _build_output(self) -> None:
        self.out = widgets.Output(
            layout=widgets.Layout(
                border="1px solid #ddd",
                padding="8px",
                height="380px",
                overflow_y="auto",
            )
        )

    def _build_inputs(self) -> None:
        self.role = widgets.Dropdown(
            options=[Role.USER.value, Role.ASSISTANT.value, Role.SYSTEM.value],
            value=Role.USER.value,
            description="Role:",
        )
        self.text = widgets.Textarea(
            placeholder="Type a message…",
            description="Content:",
            layout=widgets.Layout(width="100%", min_height="60px"),
        )
        self.btn_send = widgets.Button(
            description="Add / Send", button_style="primary"
        )
        self.btn_export = widgets.Button(description="Export JSON")

    def _build_params(self) -> None:
        self.temp = widgets.FloatSlider(
            description="temperature", min=0.1, max=1.5, step=0.05, value=0.7
        )
        self.topp = widgets.FloatSlider(
            description="top_p", min=0.1, max=1.0, step=0.01, value=0.95
        )
        self.topk = widgets.IntSlider(
            description="top_k", min=0, max=100, step=1, value=50
        )
        self.maxnt = widgets.IntSlider(
            description="max_new_tokens", min=16, max=256, step=8, value=120
        )
        self.params = widgets.Accordion(
            children=[widgets.VBox([self.temp, self.topp, self.topk, self.maxnt])]
        )
        self.params.set_title(0, "Generation parameters (role = user)")

    def _build_manage(self) -> None:
        self.sel_index = widgets.Dropdown(options=[], description="Message:")
        self.btn_delete = widgets.Button(description="Delete selected")
        self.btn_clear_all = widgets.Button(
            description="Delete ALL", button_style="danger"
        )
        self.status = widgets.HTML("")

    def _compose_layout(self) -> None:
        self.root = widgets.VBox(
            [
                self.title,
                self.out,
                widgets.VBox(
                    [
                        widgets.HBox([self.role]),
                        self.text,
                        widgets.HBox([self.btn_send, self.btn_export]),
                        self.params,
                        widgets.HTML("<hr>"),
                        widgets.HTML("<b>Manage messages</b>"),
                        widgets.HBox(
                            [self.sel_index, self.btn_delete, self.btn_clear_all]
                        ),
                        self.status,
                    ]
                ),
            ]
        )

    # ---------- Wiring ----------

    def _wire_events(self) -> None:
        self.btn_send.on_click(self._on_send)
        self.btn_export.on_click(lambda _: self._ctl.export_json())
        self.btn_delete.on_click(self._on_delete_selected)
        self.btn_clear_all.on_click(lambda _: self._ctl.clear_all())

    # ---------- Handlers ----------

    def _on_send(self, _: Any) -> None:
        text = (self.text.value or "").strip()
        if not text:
            return

        if self.role.value == Role.USER.value:
            cfg = replace(
                self._ctl.config,                    # parte de la config actual
                temperature=float(self.temp.value),  # sobrescribe con lo del slider
                top_p=float(self.topp.value),
                top_k=int(self.topk.value),
                max_new_tokens=int(self.maxnt.value),
            )                                        # max_ctx_tokens no se toca, se copia tal cual
            self._ctl.set_generation(cfg)
            self._ctl.send_user(text)
        elif self.role.value == Role.ASSISTANT.value:
            self._ctl.add_assistant(text)
        else:
            self._ctl.add_system(text)

        self.text.value = ""

    def _on_delete_selected(self, _: Any) -> None:
        idx = self.sel_index.value
        if idx is not None:
            self._ctl.delete_at(int(idx))

    # ---------- Observer ----------

    def on_event(self, event: str, payload: dict) -> None:
        """React to controller/session events."""
        if event == Event.GENERATING_START:
            self._set_status("Generating…")
        elif event == Event.GENERATING_DONE:
            self._set_status("Done.")
        elif event == Event.GENERATING_ERROR:
            self._set_status(f"Error: {payload.get('error', '')}")
        elif event == Event.EXPORT_DONE:
            self._set_status(f"Exported: {payload.get('path', '')}")
        elif event in {Event.MESSAGES_UPDATED, Event.CONFIG_CHANGED}:
            # Re-render after any session/config changes.
            self._render()
            # Set a neutral status (avoid showing export text by mistake).
            if event == Event.MESSAGES_UPDATED:
                self._set_status("Messages updated.")
            else:
                self._set_status("Config updated.")

    # ---------- Rendering ----------

    def _render(self) -> None:
        html = self._fmt.render(self._session.all())
        with self.out:
            clear_output(wait=True)
            display(HTML(html))
        self._refresh_selector()

    def _refresh_selector(self) -> None:
        opts: List[Tuple[str, int]] = [(f"{i}: {m.summary()}", i) for i, m in enumerate(self._session.all())]
        self.sel_index.options = opts
        if opts:
            current = self.sel_index.value
            valid_values = [v for _, v in opts]
            self.sel_index.value = current if current in valid_values else opts[-1][1]
        else:
            self.sel_index.value = None

    def _set_status(self, text: str) -> None:
        self.status.value = (
            f"<div style='color:#555;font-size:12px'>{text}</div>"
        )

        
