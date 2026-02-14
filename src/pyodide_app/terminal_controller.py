import js
import sys
import io
import asyncio
from typing import Any
from pyodide_app.bridge.core import keep_alive
from pyodide.ffi import create_proxy

class VirtualTerminal:
    def __init__(self, output_id: str, input_id: str):
        self.output_el = js.document.getElementById(output_id)
        self.input_el = js.document.getElementById(input_id)
        
        # Redirect stdout/stderr to this terminal
        sys.stdout = self
        sys.stderr = self
        
        self.setup_ui()

    def write(self, text: str) -> None:
        """Standard write method for file-like objects."""
        span = js.document.createElement("span")
        span.innerText = text
        self.output_el.appendChild(span)
        # Auto-scroll to bottom
        self.output_el.scrollTop = self.output_el.scrollHeight

    def flush(self) -> None:
        """Required for file-like interface."""
        pass

    async def handle_input(self, event: Any) -> None:
        if event.key == "Enter":
            command = self.input_el.value
            self.input_el.value = ""
            
            print(f">>> {command}")
            try:
                # Use pyodide.eval_code or eval for simple expressions
                # For this pattern, we just echo and demonstrate the capture
                if command.strip() == "clear":
                    self.output_el.innerHTML = ""
                else:
                    # In a real terminal, you'd use a more robust eval loop
                    result = eval(command, js.pyodide_globals)
                    if result is not None:
                        print(str(result))
            except Exception as e:
                print(f"Error: {e}")

    def setup_ui(self) -> None:
        proxy = keep_alive(create_proxy(lambda e: asyncio.ensure_future(self.handle_input(e))))
        self.input_el.addEventListener("keydown", proxy)
        print("Python Virtual Terminal Ready.")
        print("Type a Python expression (e.g. 2+2) or 'clear'.")

def init_terminal() -> None:
    # We pass the globals so eval() can access them
    js.pyodide_globals = globals()
    term = VirtualTerminal("term-output", "term-input")

init_terminal()
