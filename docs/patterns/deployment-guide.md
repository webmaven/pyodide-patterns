# Deployment & Security Headers

## Context
Advanced Pyodide features like **Shared Memory (SAB)** and **Native Multithreading** require the browser to be in a "Cross-Origin Isolated" state. This state is triggered by specific HTTP response headers.

## Problem
Most static hosting providers (GitHub Pages, Vercel, Netlify) serve pages with standard security headers that disable advanced WASM features. Configuring these headers manually for each platform can be repetitive and error-prone.

## Forces
*   **Browser Security**: COOP/COEP headers protect against side-channel attacks (like Spectre) but restrict how your page interacts with other origins.
*   **Platform Limitations**: Some platforms (like GitHub Pages) do not allow modification of HTTP response headers at all.
*   **Resource Blocking**: Enabling isolation can break third-party scripts (analytics, fonts) if they aren't configured correctly.

## Solution
Apply platform-specific configurations or use a Service Worker proxy to inject the necessary headers.

1.  **Direct Headers**: For platforms that support it (Vercel, Netlify), use their configuration files (`vercel.json`, `_headers`).
2.  **Service Worker Proxy**: For platforms that don't support custom headers (GitHub Pages), use a Service Worker to intercept requests and append the headers locally in the browser.

## Implementation
See the [Deployment Snippets](../../deployment/README.md) directory for ready-to-use files:
*   **Vercel**: `deployment/vercel.json`
*   **Netlify**: `deployment/_headers`
*   **GitHub Pages**: `deployment/github-pages/coop-coep-sw.js`

### GitHub Pages Setup (Python-friendly)
In your main HTML file:
```javascript
if ("serviceWorker" in navigator) {
    // Register the header-injecting service worker
    navigator.serviceWorker.register("coop-coep-sw.js").then(() => {
        if (!navigator.serviceWorker.controller) {
            // First visit: reload to allow SW to take control and inject headers
            window.location.reload();
        }
    });
}
```

## Resulting Context
*   **Pros**: Enables high-performance multithreading and SAB on any static host. Provides a consistent deployment path for advanced Pyodide apps.
*   **Cons**: May require a page refresh on the first visit (for Service Worker workaround). Requires careful auditing of third-party assets (must be CORS/CORP compliant).

## Related Patterns
*   **Cross-Origin Isolation**: The underlying architectural concept.
*   **Shared Memory (SAB)**: The primary feature enabled by this guide.
*   **Worker Pool**: Often depends on SAB for efficient thread coordination.
