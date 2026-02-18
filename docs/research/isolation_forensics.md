# Forensic Analysis: Cross-Origin Isolation on Static Hosts

**Status:** Resolved (v6.0.0 - Atomic Shield Pattern)
**Target:** Pyodide Multithreading on GitHub Pages

## 1. The Core Constraint
Static hosts like GitHub Pages do not allow setting the custom HTTP headers (`COOP`, `COEP`) required for a browser to enter a "Cross-Origin Isolated" state. Without this state, high-performance features like `SharedArrayBuffer` are disabled.

## 2. The Service Worker Proxy
We implemented a Service Worker (`coop-coep-sw.js`) to intercept document requests and inject the required headers. While successful for the main thread, this introduced a "Cascading Blockade" for background threads (Web Workers).

## 3. The Failure Matrix
Our Playwright Lab revealed three distinct failure modes:
1.  **CDN Blockade:** Workers loading Pyodide from a CDN failed because the CDN lacked `CORP` headers.
2.  **Service Worker Race:** Even with vendored local scripts, workers often spawned before the Service Worker established control of their sub-origin, leading to unshielded loads.
3.  **Response Identity Crisis:** Attempting to re-wrap worker scripts in the Service Worker using `new Response(buffer)` caused browsers to distrust the script's origin, killing the thread.

## 4. The Final Architectural Solution: Atomic Shield
The only 100% stable solution identified is to **remove the network** from the worker bootstrap phase.

### Mechanism:
1.  **Shielded Main Thread:** The Main Thread is proven to be isolated via the Service Worker.
2.  **In-Memory Fetch:** The Main Thread fetches the worker dependencies (`comlink`, `pyodide`) as raw text.
3.  **Blob Spawning:** These dependencies are prepended to the worker logic string, and a **Blob URL** is generated.
4.  **Automatic Inheritance:** Because the Blob is created in an already-shielded context, it inherits the parent's security status, bypassing COEP/CORP checks entirely.

## 5. Decision Log
- **Decision:** Vendor all core JS dependencies to `/examples/vendor/`.
- **Decision:** Use `window.waitForShield()` handshake before spawning any threads.
- **Decision:** Mandatory use of `spawnIsolatedWorker` (Atomic Shield) for all multithreaded patterns.
