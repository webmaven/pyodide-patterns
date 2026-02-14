# Pyodide Patterns Cookbook

![Tests](https://github.com/webmaven/pyodide-patterns/actions/workflows/test.yml/badge.svg)

A comprehensive architectural reference and "Cookbook" for building production-ready, Python-native web applications.

## Overview

This project goes beyond simple code snippets to provide a **Narrative Pattern Language** for Pyodide. Each pattern documents the **Forces** (trade-offs), the **Architectural Solution**, and the **Resulting Context** of specific implementations.

The core philosophy is **Python-Centric Development**: providing the tools to build complex, reactive, and high-performance front-ends without leaving the Python ecosystem.

## 🏛️ Narrative Pattern Language

For a deep dive into the architectural reasoning behind these implementations, see our [Pattern Index](docs/README.md).

### 1. Architectural & UI Patterns
*   **[Reactive UI (VDOM, Signals, Observer)](docs/patterns/reactive-ui.md)**: Three 100% Python implementations for syncing state to the DOM.
*   **[Synchronous-Looking Async UI](docs/patterns/python-ui-offloading.md)**: Linear Python logic that offloads heavy work to background threads using `async/await`.
*   **[Test Suite Isolation](docs/patterns/test-suite-isolation.md)**: Strategies for running Playwright and `pytest-asyncio` without event loop conflicts.
*   **[Console Log Capturing](docs/patterns/console-log-capturing.md)**: Bridging browser output to Python test reports.

### 2. High Performance & Workers
*   **[Worker Pool](docs/patterns/worker-pool.md)**: Scaling Pyodide across multiple CPU cores with task queuing.
*   **[Shared Memory (SAB)](docs/patterns/shared-memory.md)**: True zero-copy coordination between JS, Python, and the GPU.
*   **[WebGPU Compute](docs/patterns/webgpu-compute.md)**: Direct GPU acceleration for NumPy-based workloads.
*   **[Worker RPC (Comlink)](docs/patterns/worker-rpc.md)**: Object-oriented communication between main and worker threads.

### 3. Loading & Persistence
*   **[Persistent File System (IDBFS)](docs/patterns/persistence.md)**: Mounting IndexedDB so Python file I/O survives page reloads.
*   **[Bootstrapping & Warm Starts](docs/patterns/bootstrapping.md)**: Optimizing perceived performance via background loading.
*   **[Service Worker Caching](docs/patterns/service-worker-caching.md)**: Local caching of the Pyodide runtime and Python wheels.
*   **[Worker Load Failure](docs/patterns/worker-load-failure.md)**: Robust detection of network and CORS issues in workers.

## 🛠️ The Unified Python Bridge

All patterns leverage `src/pyodide_app/bridge.py`, a unified utility module that provides:
*   **`Signal`**: Fine-grained reactivity.
*   **`@observable`**: Dataclass-based state management.
*   **`PythonVDOM`**: A pure Python Virtual DOM engine.
*   **`keep_alive`**: Automatic proxy lifecycle management to prevent GC memory leaks.

## 🚀 Getting Started

### Installation

```bash
# Clone and setup environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# Build required wheels
python -m pip install build
python -m build
python -m build _my_local_package
```

### Running Tests

We use a comprehensive test suite that mirrors the pattern structure:

```bash
# Run all verified patterns
pytest tests/patterns

# Run specific category
pytest tests/patterns/architectural
```

## ✨ Engineering Standards

*   **100% Typed**: All source files use strict Python type hinting verified by `mypy`.
*   **Linted & Formatted**: Enforcement via `ruff` and `pre-commit` hooks.
*   **CI/CD Matrix**: Every pattern is tested against Pyodide versions 0.26, 0.27, and 0.28.

## Contributing

Contributions are welcome! If you have a new architectural pattern for Pyodide, please see our [contributing guide](CONTRIBUTING.md).
