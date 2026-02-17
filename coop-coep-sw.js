/*
 * High-Stability COOP/COEP/CORP Service Worker
 * Version: 2.2.0
 */

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") return;

    const url = new URL(event.request.url);
    const isSameOrigin = url.origin === self.location.origin;

    event.respondWith(
        fetch(event.request)
            .then((response) => {
                // If the response is opaque (status 0), we CANNOT read or modify headers.
                // In a COEP context, the browser will block this opaque response.
                // We must re-fetch with mode: 'cors' to get a non-opaque response.
                if (response.status === 0 && !isSameOrigin) {
                    return fetch(new Request(event.request, { mode: "cors" }))
                        .then(corsResp => {
                            const newHeaders = new Headers(corsResp.headers);
                            newHeaders.set("Cross-Origin-Resource-Policy", "cross-origin");
                            return new Response(corsResp.body, {
                                status: corsResp.status,
                                statusText: corsResp.statusText,
                                headers: newHeaders,
                            });
                        })
                        .catch(() => response); // Fallback to original if CORS fails
                }

                // If it's a 304 (Not Modified) or 204 (No Content), return as-is.
                // Re-wrapping these in 'new Response' can be problematic in some browsers.
                if (response.status === 304 || response.status === 204) {
                    return response;
                }

                const newHeaders = new Headers(response.headers);
                
                // Set CORP to cross-origin for all same-site resources too.
                newHeaders.set("Cross-Origin-Resource-Policy", "cross-origin");

                if (isSameOrigin && (
                    event.request.mode === "navigate" || 
                    (response.headers.get("content-type") && response.headers.get("content-type").includes("text/html"))
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
            .catch(() => fetch(event.request))
    );
});
