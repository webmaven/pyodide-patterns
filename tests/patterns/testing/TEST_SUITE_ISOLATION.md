# Test Suite Isolation Pattern

This pattern addresses the event loop conflict that occurs when using `pytest-asyncio` and `pytest-playwright` in the same test suite.

## The Problem

Both `pytest-asyncio` and `pytest-playwright` attempt to manage the `asyncio` event loop. When they are used together in the same process/run, it often leads to a `RuntimeError: Cannot run the event loop while another loop is running` or other event loop related failures.

This is a common issue for Pyodide applications that want to use:
- **Playwright** for End-to-End (E2E) testing.
- **pytest-asyncio** for integration/unit testing of async Python code without a browser.

## The Solution: Isolation

The most robust solution, as demonstrated by the [Imposition](https://github.com/webmaven/imposition/) project, is to isolate these two types of tests into separate test suites that are run independently.

### 1. Dedicated Directory
Place integration tests that require `pytest-asyncio` in a dedicated directory (e.g., `tests/integration/`).

### 2. Dedicated Configuration
Create a `pytest.ini` and `conftest.py` inside that directory to configure it independently.

**`tests/integration/pytest.ini`**:
```ini
[pytest]
asyncio_mode = auto
testpaths = .
```

**`tests/integration/conftest.py`**:
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

### 3. Root Exclusion
Update the root `pytest.ini` to exclude the integration directory from the main test run.

**`pytest.ini`**:
```ini
[pytest]
testpaths = tests
norecursedirs = tests/integration
```

## Running the Tests

To run all tests, you now need two commands:

1. **Main Suite (E2E & others)**:
   ```bash
   pytest
   ```

2. **Isolated Integration Suite**:
   ```bash
   pytest tests/integration
   ```

## Demonstration

The file `tests/patterns/testing/test_async_conflict_demo.py` is marked with `@pytest.mark.xfail` to demonstrate what happens when an async test is run within the main suite alongside Playwright.

The directory `tests/patterns/testing/integration/` contains a successful implementation of the isolation pattern.
