# Shared Memory (SharedArrayBuffer)

## Context
In complex Pyodide applications, data often needs to be accessed by multiple entities simultaneously: the JavaScript main thread (for UI), Python (for logic/NumPy), and the GPU (via WebGPU). Standard `ArrayBuffer` transfers involve copying data, which is slow for large datasets.

## Problem
How can we allow JavaScript and Python to read and write to the **exact same memory location** without copying, ensuring that changes made by one are immediately visible to the other?

## Forces
*   **Performance**: Copying 100MB of data between the WASM heap and the JS heap adds significant latency.
*   **Security**: `SharedArrayBuffer` requires a "Cross-Origin Isolated" environment (COOP/COEP headers).
*   **Resource Blocking**: In an isolated environment (`COEP: require-corp`), the browser will block any sub-resource (scripts, WASM, images) that does not explicitly allow it via a `Cross-Origin-Resource-Policy` header. Many CDNs do not send this header by default, which may require you to self-host the Pyodide runtime.
*   **Concurrency**: Shared memory introduces the risk of race conditions if multiple threads write to the same location without synchronization (e.g., Atomics).

## Solution
Use **`SharedArrayBuffer`** as the underlying storage. Wrap it in a TypedArray (like `Float32Array`) and pass it into Pyodide. Python can then convert this proxy into a `memoryview` or a `NumPy` array that points to the **same physical bytes**.

1.  **Isolate the Page**: Serve the page with `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp`.
2.  **Create SAB**: `const sab = new SharedArrayBuffer(size)`.
3.  **Bridge to Python**: Pass the JS TypedArray into Pyodide and use `.to_py()` to get a zero-copy memoryview.
4.  **In-Place Modification**: Use NumPy's `np.frombuffer()` to manipulate the data without allocating new memory.

## Implementation

### The Zero-Copy Bridge
```javascript
// JS Side
const sharedBuffer = new SharedArrayBuffer(1024);
const sharedView = new Float32Array(sharedBuffer);
pyodide.globals.set("js_shared_view", sharedView);
```

```python
# Python Side
import numpy as np
# Convert to zero-copy memoryview
mv = js_shared_view.to_py()
# Map numpy directly to the SAB bytes
data = np.frombuffer(mv, dtype=np.float32)
# Any change here is immediately visible in JS 'sharedView'
data += 1.0 
```

## Resulting Context
*   **Pros**: Zero-copy data sharing. Maximum possible performance for data-heavy apps.
*   **Cons**: Requires strict server header configuration. Potential for data corruption if synchronization isn't handled (use `Atomics` for thread safety).

## Related Patterns
*   **Cross-Origin Isolation**: The prerequisite for this pattern.
*   **WebGPU Compute Acceleration**: SABs are ideal for preparing data for GPU upload.

## Verification
*   **Example**: `examples/loading/shared_memory_gpu.html`
*   **Test**: `tests/patterns/workers/test_shared_array_buffer.py`
