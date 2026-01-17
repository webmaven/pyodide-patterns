# Pyodide Patterns Cookbook

A comprehensive collection of testing, debugging, and architectural patterns for building production-ready Pyodide applications.

## Overview

This project serves as a "cookbook" and reference implementation for developers working with Pyodide. It consolidates best practices for:

*   **Testing**: Robust end-to-end testing with Playwright and Pytest.
*   **Debugging**: Tactics for diagnosing issues in the browser (console logs, network errors, Web Workers).
*   **Loading**: Strategies for efficient package loading and error handling, including runtime errors.
*   **Workers**: Patterns for running Python code in Web Workers, including load failure handling.

## Project Structure

The project is organized into "patterns", each demonstrating a specific concept or solution.

```
pyodide-patterns/
├── src/                    # Python package source
├── tests/
│   └── patterns/           # The core content
│       ├── debugging/      # Debugging scenarios (race conditions, etc.)
│       ├── loading/        # Package loading and error handling
│       ├── workers/        # Web Worker patterns
│       └── testing/        # General testing patterns
└── examples/               # HTML/JS examples for the tests
```

## Getting Started

### Prerequisites

*   Python 3.8+
*   [Hatch](https://hatch.pypa.io/latest/) (recommended for project management)

### Installation

1.  Clone the repository.
2.  Install dependencies and run tests using Hatch:

```bash
hatch build
cd _my_local_package && hatch build && cd ..
hatch run test
```

Or manually with pip:

```bash
pip install pytest pytest-playwright pytest-asyncio
playwright install
pytest
```

## Patterns

### 1. Testing Patterns
*   **End-to-End Testing**: How to test full user flows in the browser.
*   **Functional Testing**: How to verify specific features.
*   **Test Suite Isolation**: How to resolve event loop conflicts between `pytest-asyncio` and `pytest-playwright` (inspired by the Imposition project).

### 2. Debugging Patterns
*   **Race Conditions**: How to identify and fix async race conditions in tests.
*   **Console Logs**: How to capture and assert against browser console logs.
*   **Network Failures**: How to simulate and test network errors (e.g., 404s).

### 3. Worker Patterns
*   **Basic Worker**: Running Pyodide in a web worker.
*   **Advanced Worker**: Handling errors and package loading inside workers.
*   **Data Cloning**: Understanding limitations of data transfer between main thread and workers.
*   **Load Failure**: Documenting the difficulty of reliably capturing worker script load failures.

### 4. Loading Patterns
*   **Package Loading**: Strategies for loading packages via `micropip`.
*   **Error Handling**: Gracefully handling load failures and runtime errors.
*   **Runtime Error**: Demonstrates handling of Python runtime errors within Pyodide.

## Contributing

Contributions are welcome! If you have a new pattern or recipe, please see our [contributing guide](CONTRIBUTING.md) for more details.
