# Worker Load Failure

## Context
When building Pyodide applications, performance best practices dictate moving the heavy initialization and execution of Python code into a **Web Worker**. This keeps the main UI thread responsive.

## Problem
Detecting when a Worker script fails to load (e.g., due to a `404 Not Found` or a CORS violation) is surprisingly difficult. The `new Worker()` constructor does not throw an exception if the script is missing, and the `worker.onerror` event often fails to fire for initial script load failures in many browsers.

## Forces
*   **Asynchronicity**: `new Worker()` returns immediately before the script is fetched.
*   **Silent Failures**: Browsers typically log a "404 Not Found" or "CORS Error" to the console, but do not provide a standard programmatic way for the main thread to catch this specific network failure.
*   **Security (CORS)**: Worker scripts must adhere to Same-Origin policy unless specific headers are present, adding another layer of potential failure.

## Solution
Since there is no "onLoadError" event, the most robust approach is a **Handshake Pattern**:

1.  **Timeout**: Set a reasonable timeout in the main thread.
2.  **Ready Message**: The Worker script should send a `"READY"` message to the main thread immediately after it successfully loads.
3.  **Fallback**: If the main thread does not receive the `"READY"` message within the timeout period, it assumes a load failure and handles it gracefully (e.g., notifying the user or falling back to the main thread).

## Implementation

### The Handshake Strategy
In your main application logic:

```javascript
const loadWorker = (url, timeoutMs = 5000) => {
    return new Promise((resolve, reject) => {
        const worker = new Worker(url);
        const timer = setTimeout(() => {
            worker.terminate();
            reject(new Error("Worker timed out while loading."));
        }, timeoutMs);

        worker.onmessage = (e) => {
            if (e.data.status === "READY") {
                clearTimeout(timer);
                resolve(worker);
            }
        };
    });
};
```

### The Worker Script (`worker.js`)
```javascript
// Send the handshake immediately
self.postMessage({ status: "READY" });

// Load Pyodide
importScripts("https://cdn.jsdelivr.net/pyodide/v0.28.0/full/pyodide.js");
// ... rest of initialization
```

## Resulting Context
*   **Pros**: Provides a reliable way to detect and recover from load failures.
*   **Cons**: Introduces a delay (the timeout) before the failure is reported. Requires the Worker script to be "aware" of the handshake protocol.

## Related Patterns
*   **Basic Worker**: The foundation for running Pyodide in the background.
*   **Worker Error Handling**: For catching Python runtime errors *after* the worker has successfully loaded.

## Verification
This failure mode is demonstrated in:
*   **Test**: `tests/patterns/workers/test_worker_load_failure.py`
*   **Example**: `examples/workers/worker_load_error.html`
