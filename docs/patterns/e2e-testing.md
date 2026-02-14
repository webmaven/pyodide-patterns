# End-to-End (E2E) Testing

## Context
The ultimate test for a Pyodide application is verifying that the Python code, the JavaScript glue code, and the browser UI all work together in harmony.

## Problem
Testing Pyodide in the browser is non-deterministic. Unlike standard web apps, you have to wait for a 10MB+ WASM runtime to download, initialize, and bootstrap the Python environment before any logic can execute. Standard timeouts often fail.

## Forces
*   **Startup Latency**: Pyodide takes time to load. Tests must be patient.
*   **Event Loop Conflicts**: If using `pytest-asyncio` and `pytest-playwright`, their event loops can clash.
*   **Observability**: Headless browsers don't show console logs or network errors by default.
*   **State Synchronization**: Verifying that a Python-initiated state change has reflected in the JS-rendered DOM.

## Solution
Use **Playwright** with **Extended Timeouts** and **State Waiters**.

1.  **Wait for Ready**: Don't start interacting until the page explicitly signals that Pyodide is ready (e.g., a "Ready" text in a status div).
2.  **Extended Timeouts**: Set `expect(locator).to_have_text(..., timeout=30000)` to account for slow runtime initialization.
3.  **Capture logs**: Use `page.on("console", ...)` to pipe browser logs into the test report for debugging.
4.  **Isolate Execution**: Run these tests in a separate suite to avoid asyncio conflicts.

## Implementation

### The E2E Pattern
```python
from playwright.sync_api import Page, expect

def test_full_scenario(page: Page, http_server):
    # 1. Capture logs for observability
    page.on("console", lambda msg: print(f"Browser: {msg.text}"))

    page.goto(f"{http_server}/index.html")

    # 2. Wait for the 'Heavy' runtime to bootstrap
    expect(page.locator("#status")).to_have_text("Pyodide Ready", timeout=30000)

    # 3. Perform user actions
    page.locator("#input").fill("Test")
    page.locator("#submit").click()

    # 4. Verify end-to-end result
    expect(page.locator("#output")).to_have_text("Result: Test")
```

## Resulting Context
*   **Pros**: High confidence. Verifies the actual user experience.
*   **Cons**: Slow execution. Brittle if timeouts aren't managed carefully.

## Related Patterns
*   **Test Suite Isolation**: Critical for stability.
*   **Console Log Capturing**: Critical for debugging failures.
*   **Worker Load Failure**: Often discovered during E2E testing.

## Verification
*   **Test**: `tests/patterns/testing/test_e2e.py`
*   **Demonstration**: `tests/patterns/testing/test_functional.py`
