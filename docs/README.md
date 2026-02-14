# Pyodide Patterns Index

This directory contains narrative documentation for the patterns implemented in this cookbook. Unlike raw code examples, these patterns explain the **Forces** and **Trade-offs** involved in building production-ready Pyodide applications.

## Table of Contents

### 1. Architectural Patterns
*   [Test Suite Isolation](./test-suite-isolation.md) - How to run Playwright and pytest-asyncio in the same project.
*   [Console Log Capturing](./console-log-capturing.md) - How to intercept and assert against browser logs.
*   [Synchronous-Looking Async UI](./python-ui-offloading.md) - Writing 100% Python UIs that offload work to background threads.
*   [Reactive UI Patterns](./reactive-ui.md) - Three ways to sync Python state with the DOM (Observer, VDOM, Signals).
*   [Deployment & Security Headers](./deployment-guide.md) - Enabling COOP/COEP on Vercel, Netlify, and GitHub Pages.

### 2. Testing Patterns
*   [Unit Testing](./unit-testing.md) - Mocking browser globals for fast logic verification.
*   [Integration Testing](./integration-testing.md) - Verifying module interactions outside the browser.
*   [End-to-End (E2E) Testing](./e2e-testing.md) - Orchestrating Playwright for full-stack verification.

### 3. Web Worker Patterns
*   [Worker Load Failure](./worker-load-failure.md) - Strategies for detecting when a worker script fails to load.
*   [Cross-Origin Isolation](./cross-origin-isolation.md) - Enabling SharedArrayBuffer and native threading.
*   [Worker RPC (Comlink)](./worker-rpc.md) - Using Comlink for clean communication between threads.
*   [Worker Pool](./worker-pool.md) - Scaling Pyodide across multiple cores with task queuing.

### 4. Loading Patterns
*   [Service Worker Caching](./service-worker-caching.md) - Using Service Workers to cache the Pyodide runtime and packages.
*   [Proxy Memory Management](./memory-management.md) - Preventing memory leaks by explicitly destroying Python-JS proxies.
*   [WebGPU Compute Acceleration](./webgpu-compute.md) - Leveraging GPU parallel processing via Python.
*   [Shared Memory (SAB)](./shared-memory.md) - True zero-copy data sharing between JS, Python, and Workers.
*   [Persistent File System (IDBFS)](./persistence.md) - Ensuring Python file I/O survives page reloads.
*   [Bootstrapping & Warm Starts](./bootstrapping.md) - Optimizing perceived performance via background loading and feedback.

## Pattern Schema
Each pattern in this library follows a strict schema inspired by Christopher Allen's Pattern Language:

*   **Context**: When does this situation arise?
*   **Problem**: What is the specific challenge?
*   **Forces**: What are the competing constraints?
*   **Solution**: The high-level strategy.
*   **Implementation**: Code snippets and links.
*   **Resulting Context**: The new state and trade-offs.
