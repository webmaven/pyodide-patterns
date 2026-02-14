# Deployment Configuration Snippets

This directory contains configuration files to help you enable **Cross-Origin Isolation** (COOP/COEP) on various hosting platforms. These headers are required for:
*   `SharedArrayBuffer` usage.
*   Native Python threading (pthreads).
*   High-performance WebGPU data transfers.

## 🚀 Platforms

### Vercel
Copy `vercel.json` to your project root.
*   **Method**: Uses the `headers` property to apply security policies to all routes.

### Netlify
Copy `_headers` to your project's publish directory (e.g., `dist/` or root).
*   **Method**: Netlify's standard custom headers file.

### GitHub Pages
GitHub Pages does not support custom headers natively. To enable isolation, you must use a **Service Worker workaround**.
1.  Copy `github-pages/coop-coep-sw.js` to your project root.
2.  Register it in your `index.html` as early as possible:
    ```javascript
    if ("serviceWorker" in navigator) {
        navigator.serviceWorker.register("coop-coep-sw.js");
    }
    ```
3.  **Note**: This requires a page reload on the first visit to take effect.

## ⚠️ Important Note on CDNs
When these headers are enabled, the browser will block any sub-resource (like the Pyodide runtime from `jsdelivr`) that doesn't send a `Cross-Origin-Resource-Policy` (CORP) header. 

**Recommendation**: Self-host the Pyodide files in your own `dist/` folder to ensure compatibility in isolated environments.
