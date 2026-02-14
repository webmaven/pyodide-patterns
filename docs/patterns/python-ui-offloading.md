# Synchronous-Looking Async UI (Offloading)

## Context
Standard browser architecture restricts DOM access to the **Main Thread**. When using Pyodide, running heavy Python logic on the main thread freezes the UI. While Web Workers solve this, they usually require complex message-passing logic in JavaScript, forcing Python developers to write "glue code" in another language.

## Problem
How can we write **UI logic in Python** that performs heavy background tasks without freezing the browser, while keeping the code clean, linear, and free of JavaScript boilerplate?

## Forces
*   **Main Thread Responsiveness**: The browser must remain interactive (scrolling, clicking).
*   **DOM Access**: Only the main thread Pyodide instance can access `js.document`.
*   **Async Complexity**: Web Workers are inherently asynchronous and event-driven.
*   **Developer Experience**: Python developers prefer `async/await` and linear flow over JS callbacks.

## Solution
Use a **Hybrid Python Pattern**:
1.  **Main Thread Python**: Handles UI events, manipulates the DOM via the `js` module, and manages the application state.
2.  **Worker Python**: Performs the "Heavy Lifting" (calculations, data processing).
3.  **The Awaitable Bridge**: Use an RPC library (like Comlink) to expose the worker to the main thread. Pyodide automatically converts JS Promises into Python Awaitables, allowing you to `await` the worker's result directly in Python.

## Implementation

### Python UI Controller (`ui_controller.py`)
```python
import js, asyncio
from pyodide.ffi import create_proxy

async def handle_click(event):
    # Update UI immediately
    js.document.getElementById("status").innerText = "Calculating..."
    
    # Offload to worker and 'wait' without blocking the UI thread
    # 'worker_bridge' is a JS Proxy made available globally
    result = await js.worker_bridge.do_heavy_work()
    
    # Update UI with result
    js.document.getElementById("output").innerText = str(result)

# Bind the async handler
click_proxy = create_proxy(lambda e: asyncio.ensure_future(handle_click(e)))
js.document.getElementById("btn").addEventListener("click", click_proxy)
```

## Resulting Context
*   **Pros**: 100% Python logic for the entire app. Responsive UI during long-running tasks. Extremely readable, linear code.
*   **Cons**: Requires two Pyodide instances (higher memory usage). Requires a small amount of initial JS bootstrapping to set up the bridge.

## Related Patterns
*   **Worker RPC**: The underlying communication mechanism.
*   **Proxy Memory Management**: Important for cleaning up event listener proxies.
*   **Worker Pool**: Can be used instead of a single worker for massive parallelism.

## Verification
*   **Example**: `examples/loading/python_ui_offloading.html`
*   **Test**: `tests/patterns/architectural/test_python_ui.py`
