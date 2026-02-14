from dataclasses import dataclass
from typing import Any
from pyodide_app.bridge.reactivity import observable
from pyodide_app.bridge import bind_to_dom

@observable
@dataclass
class AppState:
    count: int = 0
    username: str = "Python Developer"

store = AppState()

def setup_bindings() -> None:
    bind_to_dom(store, "count", "count-display")
    bind_to_dom(store, "count", "count-badge", "title")
    bind_to_dom(store, "username", "name-display")

def increment() -> None:
    store.count += 1

def update_name(event: Any) -> None:
    store.username = event.target.value

setup_bindings()
print("Unified Observer Pattern Ready")
