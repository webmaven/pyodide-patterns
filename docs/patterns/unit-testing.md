# Unit Testing Pyodide Logic

## Context
Pyodide applications often contain complex logic written in Python. To maintain high code quality and fast feedback loops, this logic should be verified with unit tests that run in a standard Python environment (outside the browser).

## Problem
Python code intended for Pyodide often imports browser-specific modules like `js` or `pyodide`. These modules do not exist in a standard Python environment, causing `ImportError` when running tests with `pytest`.

## Forces
*   **Speed**: Tests should run as fast as possible, which means avoiding browser startup.
*   **Environment**: The developer's local Python version may differ slightly from the Pyodide version.
*   **Global Scope**: The `js` and `pyodide` modules are provided by the Pyodide runtime and are globally available in the browser.

## Solution
Use **Module Mocking** to inject a "fake" `js` module into the Python module system before the application code is imported.

1.  **Mock Early**: Use `sys.modules["js"] = MagicMock()` at the very top of your test file or `conftest.py`.
2.  **Verify Logic**: Call Python functions normally and assert results.
3.  **Mock DOM Interactions**: If the Python code interacts with the DOM (e.g., `js.document`), use `unittest.mock.patch` to verify those side effects.

## Implementation

### The Mocking Pattern
```python
import sys
from unittest.mock import MagicMock

# Inject the mock before importing the app
sys.modules["js"] = MagicMock()

from my_app.logic import calculate_total

def test_calculate_total():
    assert calculate_total(10, 0.05) == 10.5
```

## Resulting Context
*   **Pros**: Extremely fast execution. No browser dependency. Focuses on pure logic.
*   **Cons**: Does not verify that the code actually works *inside* the browser's unique execution environment.

## Related Patterns
*   **Integration Testing**: Moving from logic-only to module-interaction tests.
*   **Test Suite Isolation**: Necessary if you mix these logic tests with browser tests in the same run.

## Verification
*   **Test**: `tests/patterns/testing/test_unit.py`
