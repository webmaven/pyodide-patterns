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
Use **Guarded Platform Imports** to allow Python modules to be imported in standard CPython for testing.

1.  **Environment Detection**: Use `sys.platform == 'emscripten'` to detect if the code is running in Pyodide.
2.  **Fallback Mocks**: If not in Emscripten, provide fallback mocks for `js` and `pyodide` modules.
3.  **Clean Imports**: This allows tests to import the application code directly without manual `sys.modules` manipulation.

## Implementation

### The Guarded Import Pattern
In your application code:
```python
import sys
IS_EMSCRIPTEN = sys.platform == "emscripten"

if IS_EMSCRIPTEN:
    import js
    from pyodide.ffi import create_proxy
else:
    from unittest.mock import MagicMock
    js = MagicMock()
    def create_proxy(obj): return obj
```

### The Test File
```python
# No manual mocking required in the test itself
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
