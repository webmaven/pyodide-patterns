from typing import Any

from .core import _GLOBAL_PROXIES, IS_EMSCRIPTEN, keep_alive
from .reactivity import Signal, observable
from .vdom import PythonVDOM, h

if IS_EMSCRIPTEN:
    import js
else:
    # Provide a mock for CPython unit testing
    from unittest.mock import MagicMock

    js = MagicMock()

__all__ = [
    "keep_alive",
    "_GLOBAL_PROXIES",
    "Signal",
    "observable",
    "h",
    "PythonVDOM",
    "bind_to_dom",
]

# --- UI Helpers ---


def bind_to_dom(
    state_obj: Any, field: str, element_id: str, attr: str = "innerText"
) -> None:
    """Helper to bind an observable field directly to a DOM element."""

    def update_ui(val: Any) -> None:
        el = js.document.getElementById(element_id)
        if el:
            if attr == "value":
                el.value = str(val)
            else:
                setattr(el, attr, str(val))

    state_obj.subscribe(field, update_ui)
