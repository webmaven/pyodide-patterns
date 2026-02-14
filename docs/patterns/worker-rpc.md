# Worker RPC (Comlink)

## Context
Standard Web Worker communication relies on the `postMessage` API, which is asynchronous and string-based (or structured-clone based). For complex Pyodide applications, manually managing message IDs and callback mapping for multiple distinct operations (initializing, installing packages, running scripts) becomes error-prone and "spaghetti-like."

## Problem
How can we call asynchronous Python functions inside a Worker as if they were local asynchronous methods in the main thread?

## Forces
*   **Developer Experience**: `postMessage` is low-level and hard to reason about for request-response cycles.
*   **Asynchronicity**: All Worker communication is inherently async.
*   **Structured Clone**: Data passed between threads must be compatible with the Structured Clone algorithm.

## Solution
Use a **Remote Procedure Call (RPC)** library like **Comlink**. Comlink uses JS Proxies to turn the `postMessage` interface into an object-oriented API. 

1.  **Expose**: In the Worker, use `Comlink.expose()` to make a class or object available.
2.  **Wrap**: In the main thread, use `Comlink.wrap()` to create a proxy of that object.

## Implementation

### The Worker (`comlink_worker.js`)
```javascript
importScripts("https://cdn.jsdelivr.net/npm/comlink/dist/umd/comlink.js");
importScripts("https://cdn.jsdelivr.net/pyodide/v0.28.0/full/pyodide.js");

class PyodideWorker {
    async init() {
        this.pyodide = await loadPyodide();
    }

    async runPython(code) {
        return await this.pyodide.runPythonAsync(code);
    }
}

Comlink.expose(new PyodideWorker());
```

### The Main Thread
```javascript
const worker = new Worker('comlink_worker.js');
const pyodide = Comlink.wrap(worker);

await pyodide.init();
const result = await pyodide.runPython("1 + 1");
console.log(result); // 2
```

## Resulting Context
*   **Pros**: Drastically simplifies the architecture of multi-threaded apps. Allows for clean separation of concerns.
*   **Cons**: Introduces a small dependency (Comlink). Small overhead for the proxy layer (negligible compared to Pyodide initialization).

## Related Patterns
*   **Basic Worker**: The foundation for background execution.
*   **Cross-Origin Isolation**: Often used when the RPC needs to handle shared memory.

## Verification
*   **Test**: `tests/patterns/workers/test_comlink.py`
*   **Example**: `examples/workers/comlink_rpc.html`
