# Atomic Worker Shield

Establishing a stable, multithreaded environment on static hosts by bypassing the network blockade.

## Context
Applications requiring multithreading (SharedArrayBuffer) or large-scale background computation in Pyodide, hosted on platforms that do not support custom HTTP headers (e.g., GitHub Pages).

## Forces
- **Browser Security:** COEP/COEP requirements kill threads that load unshielded scripts.
- **Static Hosting:** Inability to set server-side headers.
- **Service Worker Races:** Workers often spawn faster than a Service Worker can intercept them.
- **CDN Incompatibility:** External scripts usually lack the necessary `CORP` headers.

## Solution: The Atomic Shield
Bypass the network security check by spawning workers from in-memory Blobs that have pre-loaded dependencies.

### 1. Vendor Dependencies
Move all core JavaScript dependencies (Pyodide, Comlink) to the local origin to ensure they can be fetched as text by the main thread.

### 2. Handshake First
The main thread must verify the Service Worker is actively intercepting requests before proceeding.
```javascript
if (!(await window.waitForShield())) return;
```

### 3. Blob Bootstrap
Fetch the dependency code, prepend it to your worker logic, and spawn from a Blob URL.
```javascript
const blob = new Blob([dep1 + dep2 + workerLogic], { type: 'application/javascript' });
const worker = new Worker(URL.createObjectURL(blob));
```

## Implementation
See `examples/js/atomic_bootstrap.js` for the reusable utility and `examples/loading/python_ui_offloading.html` for a production example.

## Resulting Context
- **100% Stability:** Workers initialize correctly on the first attempt across all browsers.
- **Zero Configuration:** Works on any static host without server-side changes.
- **Maximum Performance:** Enables `SharedArrayBuffer` and multithreading in restrictive environments.
