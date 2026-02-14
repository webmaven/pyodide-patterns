import sys
import asyncio
from typing import Any
from pyodide_app.bridge.core import IS_EMSCRIPTEN

if IS_EMSCRIPTEN:
    import js
    from pyodide.ffi import create_proxy
else:
    from unittest.mock import MagicMock
    js = MagicMock()
    def create_proxy(obj: Any) -> Any:
        return obj

async def handle_click(event: Any) -> None:
    button = js.document.getElementById("process-btn")
    output = js.document.getElementById("ui-output")
    status = js.document.getElementById("ui-status")
    
    # 1. Update UI immediately (Main Thread)
    button.disabled = True
    status.innerText = "Worker calculating (3s sleep)..."
    output.innerText = "..."
    
    try:
        # 2. Call the worker (Offloaded)
        # This looks linear/synchronous but is actually an async bridge
        # We call the JS 'worker_bridge' which is a Comlink proxy
        result = await js.worker_bridge.runPython("import time; time.sleep(3); 'The answer is 84'")
        
        # 3. Update UI with result (Main Thread)
        output.innerText = str(result)
        status.innerText = "Computation complete."
    except Exception as e:
        status.innerText = f"Error: {str(e)}"
    finally:
        button.disabled = False

def setup_ui() -> None:
    # Bind the Python function to the JS button
    click_proxy = create_proxy(lambda e: asyncio.ensure_future(handle_click(e)))
    js.document.getElementById("process-btn").addEventListener("click", click_proxy)
    js.document.getElementById("ui-status").innerText = "Python UI Controller Ready."

# Global entry point
setup_ui()
