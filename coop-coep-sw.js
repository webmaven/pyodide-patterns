/*
 * COOP/COEP Service Worker Workaround for GitHub Pages
 * This version is designed to be more aggressive in enabling isolation
 * while ensuring that external CDNs aren't blocked.
 */

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

self.addEventListener("fetch", (event) => {
    if (event.request.cache === "only-if-cached" && event.request.mode !== "same-origin") {
        return;
    }

    event.respondWith(
        fetch(event.request)
            .then((response) => {
                if (response.status === 0) {
                    // Opaque response (no CORS headers from server)
                    // We can't modify headers, but the browser will block it 
                    // in an isolated environment anyway.
                    return response;
                }

                const newHeaders = new Headers(response.headers);
                
                // Add COOP/COEP to same-origin HTML responses
                const isHtml = response.headers.get("content-type")?.includes("text/html");
                const isSameOrigin = new URL(event.request.url).origin === self.location.origin;
                
                if (isSameOrigin && isHtml) {
                    newHeaders.set("Cross-Origin-Embedder-Policy", "require-corp");
                    newHeaders.set("Cross-Origin-Opener-Policy", "same-origin");
                }

                // CRITICAL: Set CORP to 'cross-origin' for everything we can.
                // This tells the browser: "I am aware of the isolation, please allow this resource."
                newHeaders.set("Cross-Origin-Resource-Policy", "cross-origin");

                return new Response(response.body, {
                    status: response.status,
                    statusText: response.statusText,
                    headers: newHeaders,
                });
            })
            .catch((e) => {
                console.error("SW Fetch Error for:", event.request.url, e);
                return fetch(event.request); // Fallback to original request
            })
    );
});
