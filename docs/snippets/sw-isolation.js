/*
 * COOP/COEP Isolation Service Worker - Self-Contained Snippet
 * 
 * Instructions:
 * 1. Save as 'coop-coep-sw.js' in project root.
 * 2. Register: navigator.serviceWorker.register('./coop-coep-sw.js');
 */
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") return;
    const url = new URL(event.request.url);
    if (url.origin !== self.location.origin) return;

    event.respondWith(
        fetch(event.request).then((response) => {
            if (response.status === 0 || response.status === 304) return response;
            const newHeaders = new Headers(response.headers);
            newHeaders.set("Cross-Origin-Resource-Policy", "cross-origin");
            if (event.request.mode === "navigate" || response.headers.get("content-type")?.includes("text/html")) {
                newHeaders.set("Cross-Origin-Embedder-Policy", "require-corp");
                newHeaders.set("Cross-Origin-Opener-Policy", "same-origin");
            }
            return new Response(response.body, { status: response.status, statusText: response.statusText, headers: newHeaders });
        }).catch(() => fetch(event.request))
    );
});
