# Service Worker Caching

## Context
Pyodide is a large runtime (approx. 10MB+ for the core WASM and standard library). Loading these assets from a CDN on every page visit or during development can lead to slow "cold starts" and significant bandwidth usage.

## Problem
How can we ensure that the Pyodide runtime and heavy Python wheels (like `numpy`) are loaded instantly for returning users, even in poor network conditions or offline?

## Forces
*   **Asset Size**: WASM and ZIP files are large and benefit significantly from local caching.
*   **Cold Start Latency**: The time-to-interactive for a Pyodide app is dominated by network download time.
*   **Versioning**: When Pyodide is updated on the CDN, the cache must be correctly invalidated to prevent version mismatch errors.

## Solution
Implement a **Service Worker** to intercept network requests and serve Pyodide assets from the **Cache Storage API**.

1.  **Intercept**: The Service Worker listens for `fetch` events.
2.  **Match**: If the request URL matches a known Pyodide CDN asset, check the local cache.
3.  **Serve or Cache**: Return the cached version if it exists; otherwise, fetch it from the network and store it in the cache for future use (Cache-First or Stale-While-Revalidate strategy).

## Implementation

### The Service Worker (`service_worker.js`)
```javascript
const CACHE_NAME = 'pyodide-v1';
const ASSETS = [
    'https://cdn.jsdelivr.net/pyodide/v0.28.0/full/pyodide.js',
    'https://cdn.jsdelivr.net/pyodide/v0.28.0/full/pyodide.asm.wasm',
    // ... other assets
];

self.addEventListener('fetch', (event) => {
    if (event.request.url.includes('cdn.jsdelivr.net')) {
        event.respondWith(
            caches.match(event.request).then((cached) => {
                return cached || fetch(event.request).then((response) => {
                    return caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, response.clone());
                        return response;
                    });
                });
            })
        );
    }
});
```

### Registration (Main Thread)
```javascript
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/js/service_worker.js');
}
```

## Resulting Context
*   **Pros**: Instant loading for returning users. Enables full offline support. Reduces CDN costs and reliance.
*   **Cons**: Complexity of managing cache invalidation. Service Workers require HTTPS (except on localhost). First-load is still slow (it must be cached).

## Related Patterns
*   **Package Loading**: Service Workers can also cache `.whl` files fetched via `micropip`.
*   **Cross-Origin Isolation**: Ensure the Service Worker script is served with the correct headers if used in an isolated environment.

## Testing Limitations
Service Workers can be difficult to verify in automated testing environments (like headless Playwright or CI). They often require:
*   A "Secure Context" (HTTPS or `localhost`).
*   Persistent storage permissions.
*   Browser reloads to allow the Service Worker to take control of the client.

In many CI environments, `navigator.serviceWorker.ready` may time out or `navigator.serviceWorker.controller` may remain null despite registration.

## Verification
*   **Test**: `tests/patterns/loading/test_service_worker.py` (Note: Often fails in headless environments)
*   **Example**: `examples/loading/service_worker_cache.html`
