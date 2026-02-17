/*
 * Pass-Through Shield COOP/COEP/CORP Service Worker
 * Version: 2.3.2 (Stable Isolation)
 */

const VERSION = "2.3.2";
const log = (...args) => console.log(`[${new Date().toISOString()}] [SW v${VERSION}]`, ...args);

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") return;

    const url = new URL(event.request.url);
    const isSameOrigin = url.origin === self.location.origin;

    event.respondWith(
        fetch(event.request, isSameOrigin ? {} : { mode: "cors" })
            .then((response) => {
                // If it's a 304, we must return it as-is (browsers don't allow modifying 304s)
                // but 304s will use the headers from the previously cached 200.
                if (response.status === 304) return response;

                // Create a new set of headers from the original
                const newHeaders = new Headers(response.headers);
                
                // MANDATORY: Every resource must have CORP in an isolated environment.
                newHeaders.set("Cross-Origin-Resource-Policy", "cross-origin");

                // MANDATORY: Documents must have COOP/COEP.
                if (isSameOrigin && (
                    event.request.mode === "navigate" || 
                    response.headers.get("content-type")?.includes("text/html")
                )) {
                    newHeaders.set("Cross-Origin-Embedder-Policy", "require-corp");
                    newHeaders.set("Cross-Origin-Opener-Policy", "same-origin");
                }

                // Return a new response with the injected headers
                // We use the same status and body to ensure transparency
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
