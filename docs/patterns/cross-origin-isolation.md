# Cross-Origin Isolation (SharedArrayBuffer)

## Context
High-performance Pyodide applications often require native multithreading (via Python's `threading` module, which maps to WebAssembly pthreads). This functionality depends on `SharedArrayBuffer` to allow memory sharing between the main thread and workers.

## Problem
Due to security vulnerabilities like Spectre, browsers disable `SharedArrayBuffer` by default. To enable it, the page must be in a **cross-origin isolated** state. Achieving this state requires specific HTTP response headers that restrict how the page interacts with other origins.

## Forces
*   **Security**: `SharedArrayBuffer` can be used for high-precision timing attacks if not isolated.
*   **Performance**: Native threading is impossible without it.
*   **Compatibility**: Enabling these headers can break third-party scripts (like analytics or fonts) that do not support Cross-Origin Resource Policy (CORP).

## Solution
Configure the web server to send two specific headers for the top-level document:
1.  `Cross-Origin-Opener-Policy: same-origin` (COOP)
2.  `Cross-Origin-Embedder-Policy: require-corp` (COEP)

Additionally, any sub-resources (scripts, images) from other origins must be served with `Cross-Origin-Resource-Policy: cross-origin` or a similar permissive header.

## Implementation

### Server Configuration (Python/Pytest)
In your `conftest.py`, you can implement a custom handler to simulate this environment:

```python
class CrossOriginIsolatedHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        super().end_headers()
```

### Client-Side Detection
You can check the isolation state programmatically in JavaScript:

```javascript
if (window.crossOriginIsolated) {
    console.log("Environment is isolated. SharedArrayBuffer is available.");
} else {
    console.warn("Not isolated. Threading will be disabled.");
}
```

## Resulting Context
*   **Pros**: Enables `SharedArrayBuffer` and high-performance multithreading.
*   **Cons**: Breaks integration with third-party resources that don't send `CORP` headers. Can be difficult to configure in environments like GitHub Pages or shared hosting.

## Related Patterns
*   **Advanced Worker**: Often used in conjunction with threading.
*   **Worker Load Failure**: Isolation can sometimes cause subtle load failures for cross-origin worker scripts.

## Verification
*   **Test**: `tests/patterns/workers/test_shared_array_buffer.py`
*   **Example**: `examples/workers/shared_array_buffer.html`
