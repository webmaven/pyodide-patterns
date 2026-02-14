/*
 * Stable COOP/COEP Service Worker
 * Ensures same-origin documents are isolated.
 */

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") return;

    const url = new URL(event.request.url);
    if (url.origin !== self.location.origin) return;

    event.respondWith(
        fetch(event.request).then((response) => {
            if (!response || response.status === 0) return response;

            const newHeaders = new Headers(response.headers);
            
            // Apply isolation headers to all local resources
            newHeaders.set("Cross-Origin-Embedder-Policy", "require-corp");
            newHeaders.set("Cross-Origin-Opener-Policy", "same-origin");
            newHeaders.set("Cross-Origin-Resource-Policy", "cross-origin");

            return new Response(response.body, {
                status: response.status,
                statusText: response.statusText,
                headers: newHeaders,
            });
        }).catch(err => {
            console.error("SW Fetch Error:", err);
            return fetch(event.request);
        })
    );
});
