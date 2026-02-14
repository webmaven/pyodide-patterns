import sys
from typing import Any
from pyodide_app.bridge.reactivity import Signal
from pyodide_app.bridge.core import IS_EMSCRIPTEN, keep_alive

if IS_EMSCRIPTEN:
    import js
    from pyodide.ffi import create_proxy
else:
    from unittest.mock import MagicMock
    js = MagicMock()
    def create_proxy(obj: Any) -> Any:
        return obj

# Core Signals
count: Signal[int] = Signal(0)
theme: Signal[str] = Signal("light")

def setup_signals() -> None:
    # Subscriber 1: Update text
    count.subscribe(lambda v: setattr(js.document.getElementById("sig-count"), "innerText", str(v)))
    
    # Subscriber 2: Update calculation
    count.subscribe(lambda v: setattr(js.document.getElementById("sig-double"), "innerText", str(v * 2)))
    
    # Subscriber 3: Update CSS
    def update_theme(v: Any) -> None:
        card = js.document.getElementById("sig-card")
        if card:
            card.style.backgroundColor = "#fff" if v == "light" else "#333"
            card.style.color = "#000" if v == "light" else "#fff"
    theme.subscribe(update_theme)

def increment(event: Any) -> None:
    count.value += 1

def toggle_theme(event: Any) -> None:
    theme.value = "dark" if theme.value == "light" else "light"

def setup_ui() -> None:
    inc_btn = js.document.getElementById("sig-inc")
    if inc_btn:
        # Use bridge helper to keep event listeners alive
        inc_btn.onclick = keep_alive(create_proxy(increment))
    
    theme_btn = js.document.getElementById("sig-theme")
    if theme_btn:
        theme_btn.onclick = keep_alive(create_proxy(toggle_theme))

setup_signals()
setup_ui()
print("Unified Signals Pattern Ready")
