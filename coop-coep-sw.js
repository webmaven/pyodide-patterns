/*
 * Robust COOP/COEP/CORP Service Worker
 * Version: 2.0.0
 */

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") return;

    const url = new URL(event.request.url);
    const isSameOrigin = url.origin === self.location.origin;

    // Use CORS for cross-origin to allow header injection
    const request = isSameOrigin ? event.request : new Request(event.request, {
        mode: "cors",
        credentials: "omit"
    });

    event.respondWith(
        fetch(request).then((response) => {
            if (!response || response.status === 0) return response;

            const newHeaders = new Headers(response.headers);
            
            // 1. Mandatory for COEP: CORP header
            newHeaders.set("Cross-Origin-Resource-Policy", "cross-origin");

            // 2. Mandatory for Isolation: COOP/COEP on the document
            if (isSameOrigin && (
                event.request.mode === "navigate" || 
                response.headers.get("content-type")?.includes("text/html")
            )) {
                newHeaders.set("Cross-Origin-Embedder-Policy", "require-corp");
                newHeaders.set("Cross-Origin-Opener-Policy", "same-origin");
                newHeaders.set("Cache-Control", "no-cache, no-store, must-revalidate");
            }

            // 3. Handle 304 and other no-body responses
            const body = (response.status === 204 || response.status === 304) 
                ? null 
                : response.body;

            return new Response(body, {
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
