from typing import Any
from pyodide_app.bridge.vdom import PythonVDOM, h

class CounterApp:
    def __init__(self, engine: PythonVDOM) -> None:
        self.engine = engine
        self.count = 0

    def increment(self, event: Any) -> None:
        self.count += 1
        self.update()

    def reset(self, event: Any) -> None:
        self.count = 0
        self.update()

    def render(self) -> Any:
        # Event handlers are automatically wrapped in proxies by PythonVDOM engine
        return h("div", {"class": "card"}, [
            h("h2", {}, "Pure Python VDOM"),
            h("p", {}, f"Count: {self.count}"),
            h("button", {"onclick": self.increment}, "Increment"),
            h("button", {"onclick": self.reset}, "Reset")
        ])

    def update(self) -> None:
        self.engine.patch(self.render())

# Initialization
engine = PythonVDOM("vdom-root")
app = CounterApp(engine)
app.update()
print("Unified VDOM Pattern Ready")
