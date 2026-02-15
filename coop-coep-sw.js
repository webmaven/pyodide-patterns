/*
 * Universal COOP/COEP/CORP Service Worker
 * This version uses a Safe-Proxy pattern to ensure both local and CDN 
 * resources are compatible with a Cross-Origin Isolated environment.
 */

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") return;

    const url = new URL(event.request.url);
    const isSameOrigin = url.origin === self.location.origin;

    // Use the original request for same-origin to avoid 'mode: navigate' errors.
    // For cross-origin (CDNs), we use a new request with 'cors' mode to allow header injection.
    const request = isSameOrigin ? event.request : new Request(event.request, {
        mode: "cors",
        credentials: "omit"
    });

    event.respondWith(
        fetch(request).then((response) => {
            if (!response || response.status === 0) return response;

            const newHeaders = new Headers(response.headers);
            
            // 1. Force the browser to allow this resource in an isolated context
            newHeaders.set("Cross-Origin-Resource-Policy", "cross-origin");

            // 2. If same-origin document, enforce isolation headers
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
        }).catch(err => {
            console.error("SW Proxy Error:", url.href, err);
            return fetch(event.request);
        })
    );
});
