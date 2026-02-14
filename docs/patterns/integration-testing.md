# Integration Testing

## Context
Once individual functions are verified via unit tests, you need to ensure that different parts of your Python application (e.g., a "main" controller and a "utils" helper) interact correctly.

## Problem
In a Pyodide environment, components often interact via global state or the DOM. Verifying these interactions without a full browser can be challenging.

## Forces
*   **Module Boundaries**: Verifying that data flows correctly between Python modules.
*   **Mock Complexity**: Over-mocking can lead to tests that pass but don't reflect reality.
*   **Environment**: Like unit tests, these usually run outside the browser for speed.

## Solution
Combine **Module Mocking** with **Partial Patching**. Verify that the "Controller" module calls the "Helper" module with the expected arguments and correctly handles the return values.

1.  **Inject Mock Globals**: Continue to mock `js` and `pyodide`.
2.  **Use Real Dependencies**: Import actual dependent modules unless they perform expensive I/O.
3.  **Assert Interaction**: Use `patch` to track calls between internal Python modules.

## Implementation

### Verifying Module Interaction
```python
from unittest.mock import patch, MagicMock
from my_app.main import run_logic

def test_run_logic_integration():
    with patch("my_app.main.utils.format_data") as mock_formatter:
        mock_formatter.return_value = "Mocked Data"
        
        result = run_logic()
        
        mock_formatter.assert_called_once()
        assert "Mocked Data" in result
```

## Resulting Context
*   **Pros**: Catches bugs in internal API contracts. Fast execution.
*   **Cons**: Still doesn't verify the Python-JS bridge or browser-specific behaviors.

## Related Patterns
*   **Unit Testing**: The foundation for integration tests.
*   **End-to-End Testing**: The next step for full verification.

## Verification
*   **Test**: `tests/patterns/testing/test_integration.py`
