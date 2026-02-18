/*
 * Total Shield COOP/COEP/CORP Service Worker
 * Version: 6.0.0 (Atomic Shield)
 */

const VERSION = "6.0.0";

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") return;

    const url = new URL(event.request.url);
    const isSameOrigin = url.origin === self.location.origin;

    if (url.pathname.endsWith("/__ping__")) {
        event.respondWith(new Response("pong", { headers: { "Content-Type": "text/plain" } }));
        return;
    }

    if (!isSameOrigin) return;

    event.respondWith(
        fetch(event.request).then((response) => {
            if (response.status === 0 || response.status === 304) return response;

            const newHeaders = new Headers(response.headers);
            newHeaders.set("Cross-Origin-Resource-Policy", "cross-origin");

            if (event.request.mode === "navigate" || response.headers.get("content-type")?.includes("text/html")) {
                newHeaders.set("Cross-Origin-Embedder-Policy", "require-corp");
                newHeaders.set("Cross-Origin-Opener-Policy", "same-origin");
            }

            // Stream-safe re-wrapping
            const { readable, writable } = new TransformStream();
            response.body.pipeTo(writable);

            return new Response(readable, {
                status: response.status,
                statusText: response.statusText,
                headers: newHeaders,
            });
        }).catch(() => fetch(event.request))
    );
});
