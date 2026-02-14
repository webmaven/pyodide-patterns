# Proxy Memory Management

## Context
When data or objects are passed between Python and JavaScript in Pyodide, they are wrapped in **Proxies**. A JavaScript `PyProxy` represents a Python object, and a Python `JsProxy` represents a JavaScript object.

## Problem
JavaScript and Python have separate garbage collectors. When a Python object is proxied into JavaScript, the Python garbage collector cannot reclaim that object as long as the JavaScript proxy exists. However, the JavaScript GC does not know the size or importance of the underlying Python object, often leading to significant memory leaks in the WASM heap before the JS GC even decides to run.

## Forces
*   **Dual Garbage Collectors**: JS GC and Python GC operate independently and are unaware of each other's heap pressure.
*   **WASM Heap Limits**: The WASM memory space is finite. Leaks here are more critical than in general JS memory.
*   **Performance**: Repeatedly creating proxies without destroying them can quickly lead to `MemoryError` or sluggish performance.

## Solution
Use **Explicit Destruction** for any Python object passed to JavaScript.

1.  **Manual Destroy**: Call `.destroy()` on every `PyProxy` once you are finished with it.
2.  **Conversion**: If you only need the data, convert the proxy to a native JS object using `.toJs()` and then destroy the proxy immediately.
3.  **Try-Finally**: Use `try...finally` blocks to ensure `.destroy()` is called even if an error occurs.

## Implementation

### The Manual Cleanup Pattern
```javascript
const proxy = pyodide.runPython("some_python_function()");
try {
    // Work with the proxy
    console.log(proxy.get("key"));
} finally {
    // Explicitly release the Python object
    proxy.destroy();
}
```

### The Conversion Pattern (Best for Data)
```javascript
// Convert to native JS and destroy the proxy in one go
const data = pyodide.runPython("some_dict").toJs();
// 'data' is now a standard JS Map/Object, no cleanup needed
```

## Resulting Context
*   **Pros**: Prevents memory leaks in the WASM heap. Keeps application performance stable over long sessions.
*   **Cons**: Requires manual discipline. Forgetting a single `destroy()` in a loop can still cause a leak.

## Related Patterns
*   **Advanced Worker**: Memory management is even more critical in long-running background workers.
*   **Loading Patterns**: Efficient package loading also benefits from reclaiming memory of temporary objects used during initialization.

## Verification
*   **Test**: `tests/patterns/loading/test_memory.py`
*   **Example**: `examples/loading/proxy_management.html`
