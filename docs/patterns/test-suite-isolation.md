# Test Suite Isolation

## Context
When testing Pyodide applications, you often need two types of tests:
1.  **End-to-End (E2E) Tests**: Using Playwright to verify the browser-based UI and Python-JS integration.
2.  **Async Integration Tests**: Using `pytest-asyncio` to verify Python logic that may involve async/await, without the overhead of a browser.

## Problem
Both `pytest-playwright` and `pytest-asyncio` attempt to manage the global `asyncio` event loop. When run in the same session, they often collide, resulting in `RuntimeError: Cannot run the event loop while another loop is running` or hanging test suites.

## Forces
*   **Single Loop Constraint**: Python's `asyncio` loop is usually per-thread/process; both plugins want control of it.
*   **Developer Experience**: Developers want a single command to run all tests, but standard `pytest` execution makes this difficult when conflicts exist.
*   **Environment Mocking**: Integration tests need to mock browser-specific globals like `js` and `pyodide` which are only available inside the browser.

## Solution
Isolate the test suites into **separate physical directories** with **independent configurations**. This ensures that the event loop initialization for one suite never interferes with the other.

1.  **Dedicated Directory**: Place integration tests in a specific folder (e.g., `tests/integration/`).
2.  **Local Configuration**: Create a `pytest.ini` and `conftest.py` inside that folder to isolate its settings.
3.  **Root Exclusion**: Configure the root `pytest.ini` to ignore the isolated directory by default.

## Implementation

### Isolated Configuration (`tests/integration/pytest.ini`)
```ini
[pytest]
asyncio_mode = auto
testpaths = .
```

### Mocking Browser Globals (`tests/integration/conftest.py`)
```python
import sys
from unittest.mock import MagicMock
import nest_asyncio

# Mock browser-specific modules
sys.modules["js"] = MagicMock()
sys.modules["pyodide"] = MagicMock()

def pytest_configure(config):
    nest_asyncio.apply()
```

## Resulting Context
*   **Pros**: Rock-solid test stability. No more mysterious event loop crashes.
*   **Cons**: Requires two separate test execution commands (or a wrapper script/Makefile).

## Verification
*   **Demonstration of Conflict**: `tests/patterns/architectural/test_async_conflict_demo.py` (marked as `xfail`).
*   **Implementation of Solution**: `tests/patterns/testing/integration/` directory.
