# Pyodide Production Checklist

Ensuring stability, security, and performance for browser-native Python.

## 1. Infrastructure (GitHub Pages / Static Hosts)
- [ ] **.nojekyll:** Exists at root to prevent underscores from breaking imports.
- [ ] **MIME Types:** Ensure `.wasm` is served as `application/wasm` and `.py` as `text/plain`.
- [ ] **Cross-Origin Isolation:** Service Worker registered and actively injecting COOP/COEP headers.

## 2. Multithreading & Workers
- [ ] **Sentinel Handshake:** Main thread verifies SW interception via `waitForShield()` before spawning workers.
- [ ] **Atomic Shield:** Workers spawned from local Blobs to bypass COEP/CORP race conditions.
- [ ] **Vendored Core:** Pyodide and Comlink loaded from local origin, not external CDNs.

## 3. Lifecycle & UX
- [ ] **Progressive Loading:** UI feedback provided during the "Cold Start" (WASM download).
- [ ] **Memory Management:** JS-Python proxies explicitly `.destroy()`ed to prevent heap leaks.
- [ ] **Persistence:** IDBFS mounted and `syncfs` called after critical file writes.

## 4. Verification
- [ ] **Test Lab:** Application passes the 3-step stability matrix (Cold Start, Soft Reload, Navigation).
- [ ] **Console Health:** Zero `SyntaxError` or `COEP` related warnings in the production origin.
