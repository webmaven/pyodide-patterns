/*
 * Unbreakable Shield COOP/COEP/CORP Service Worker
 * Version: 2.3.4 (Stable Isolation)
 */

const VERSION = "2.3.4";
const log = (...args) => console.log(`[${new Date().toISOString()}] [SW v${VERSION}]`, ...args);

self.addEventListener("install", () => {
    log("Installing...");
    self.skipWaiting();
});

self.addEventListener("activate", (event) => {
    log("Activating and claiming clients...");
    event.waitUntil(self.clients.claim());
});

self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") return;

    const url = new URL(event.request.url);
    const isSameOrigin = url.origin === self.location.origin;

    event.respondWith(
        fetch(event.request, isSameOrigin ? {} : { mode: "cors" })
            .then((response) => {
                // We no longer skip 304s. We MUST ensure the headers are present.
                // However, creating a new Response with status 304 and a body is illegal.
                // So we only re-wrap if it's not a 304, or we force the headers.
                
                const newHeaders = new Headers(response.headers);
                newHeaders.set("Cross-Origin-Resource-Policy", "cross-origin");

                if (isSameOrigin && (
                    event.request.mode === "navigate" || 
                    response.headers.get("content-type")?.includes("text/html")
                )) {
                    newHeaders.set("Cross-Origin-Embedder-Policy", "require-corp");
                    newHeaders.set("Cross-Origin-Opener-Policy", "same-origin");
                }

                if (response.status === 304 || response.status === 204) {
                    // Browsers usually don't allow modifying 304 headers in the SW,
                    // so we rely on the cache-buster in the request to avoid 304s 
                    // for critical resources.
                    return response;
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
