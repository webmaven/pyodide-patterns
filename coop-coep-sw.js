/*
 * Stable COOP/COEP/CORP Service Worker
 * This version safely handles navigation requests and injects headers
 * to guarantee a Cross-Origin Isolated environment.
 */

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") return;

    const url = new URL(event.request.url);
    const isSameOrigin = url.origin === self.location.origin;

    // Construct the fetch options
    const fetchOptions = {
        // We only use 'cors' for cross-origin to allow header modification.
        // For same-origin (especially navigation), we MUST NOT override the mode.
        mode: isSameOrigin ? event.request.mode : "cors",
        credentials: event.request.credentials,
        redirect: "follow"
    };

    event.respondWith(
        fetch(event.request, isSameOrigin ? {} : fetchOptions)
            .then((response) => {
                // If the response is opaque (e.g., from a CDN without CORS),
                // we can't read or modify headers. We just return it.
                if (!response || response.status === 0) return response;

                const newHeaders = new Headers(response.headers);
                
                // 1. Always apply CORP to same-origin resources so they can be loaded
                // in an isolated context.
                if (isSameOrigin) {
                    newHeaders.set("Cross-Origin-Resource-Policy", "same-origin");
                } else {
                    // For cross-origin (CDNs), we set 'cross-origin'
                    newHeaders.set("Cross-Origin-Resource-Policy", "cross-origin");
                }

                // 2. If it's a same-origin HTML document (navigation), inject master headers.
                if (isSameOrigin && (
                    event.request.mode === "navigate" || 
                    response.headers.get("content-type")?.includes("text/html")
                )) {
                    newHeaders.set("Cross-Origin-Embedder-Policy", "require-corp");
                    newHeaders.set("Cross-Origin-Opener-Policy", "same-origin");
                    newHeaders.set("Cache-Control", "no-cache, no-store, must-revalidate");
                }

                return new Response(response.body, {
                    status: response.status,
                    statusText: response.statusText,
                    headers: newHeaders,
                });
            })
            .catch((err) => {
                console.error("SW Proxy Error:", url.href, err);
                return fetch(event.request);
            })
    );
});
