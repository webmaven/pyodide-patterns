/*
 * Definitive COOP/COEP Service Worker
 * Ensures Cross-Origin Isolation for all same-origin navigation and resources.
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
            
            // Standard Isolation Headers
            newHeaders.set("Cross-Origin-Embedder-Policy", "require-corp");
            newHeaders.set("Cross-Origin-Opener-Policy", "same-origin");
            newHeaders.set("Cross-Origin-Resource-Policy", "cross-origin");
            
            // Prevent browser from caching 'naked' versions of the page
            if (event.request.mode === "navigate") {
                newHeaders.set("Cache-Control", "no-cache, no-store, must-revalidate");
            }

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
