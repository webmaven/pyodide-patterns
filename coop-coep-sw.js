/*
 * Definitive COOP/COEP Service Worker
 * Ensures Cross-Origin Isolation for GitHub Pages.
 */

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") return;

    const url = new URL(event.request.url);
    
    // Only intercept same-origin requests to avoid breaking external CDNs
    if (url.origin !== self.location.origin) return;

    event.respondWith(
        fetch(event.request, { 
            // Bypass browser cache for the initial document to ensure we can inject headers
            cache: event.request.mode === "navigate" ? "no-store" : "default" 
        }).then((response) => {
            if (!response || response.status === 0) return response;

            const newHeaders = new Headers(response.headers);
            
            // Set headers for all same-origin resources
            newHeaders.set("Cross-Origin-Embedder-Policy", "require-corp");
            newHeaders.set("Cross-Origin-Opener-Policy", "same-origin");
            newHeaders.set("Cross-Origin-Resource-Policy", "cross-origin");
            
            // Prevent browser from caching the 'naked' or potentially stale headers
            newHeaders.set("Cache-Control", "no-cache, no-store, must-revalidate");

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
