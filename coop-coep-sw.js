/*
 * COOP/COEP Service Worker Workaround for GitHub Pages
 * This version ensures all same-origin resources are served with the 
 * necessary headers to maintain a Cross-Origin Isolated state.
 */

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

self.addEventListener("fetch", (event) => {
    // Avoid intercepting non-GET requests or external CDNs that might break
    if (event.request.method !== "GET") return;
    
    const url = new URL(event.request.url);
    const isSameOrigin = url.origin === self.location.origin;

    if (event.request.cache === "only-if-cached" && event.request.mode !== "same-origin") {
        return;
    }

    event.respondWith(
        fetch(event.request)
            .then((response) => {
                if (response.status === 0) return response;

                const newHeaders = new Headers(response.headers);
                
                // CRITICAL: Always set CORP to 'cross-origin' for everything on our origin.
                // This allows isolated pages to load these local resources.
                if (isSameOrigin) {
                    newHeaders.set("Cross-Origin-Resource-Policy", "cross-origin");
                }

                // If this is a navigation request (the HTML page itself), 
                // we MUST inject the isolation headers.
                if (isSameOrigin && (
                    event.request.mode === "navigate" || 
                    response.headers.get("content-type")?.includes("text/html")
                )) {
                    newHeaders.set("Cross-Origin-Embedder-Policy", "require-corp");
                    newHeaders.set("Cross-Origin-Opener-Policy", "same-origin");
                }

                return new Response(response.body, {
                    status: response.status,
                    statusText: response.statusText,
                    headers: newHeaders,
                });
            })
            .catch((e) => {
                console.error("SW Fetch Error:", e);
                return fetch(event.request);
            })
    );
});
