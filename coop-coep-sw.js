/*
 * Canonical COOP/COEP Service Worker for GitHub Pages
 */

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") return;

    event.respondWith(
        fetch(event.request).then((response) => {
            if (!response || response.status === 0) return response;

            const newHeaders = new Headers(response.headers);
            
            // Set headers for ALL resources to guarantee compatibility
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
