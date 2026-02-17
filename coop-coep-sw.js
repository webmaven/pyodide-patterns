/*
 * Total Shield COOP/COEP/CORP Service Worker
 * Version: 2.3.0
 */

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") return;

    const url = new URL(event.request.url);
    const isSameOrigin = url.origin === self.location.origin;

    event.respondWith(
        fetch(event.request, isSameOrigin ? {} : { mode: "cors" })
            .then((response) => {
                // If it's an opaque response (status 0), we can't do anything.
                // But since we use mode: 'cors' for cross-origin, we shouldn't get status 0
                // for CORS-supporting CDNs like jsdelivr.
                if (!response || response.status === 0) return response;

                const newHeaders = new Headers(response.headers);
                
                // MANDATORY: Every resource must have CORP in an isolated environment.
                newHeaders.set("Cross-Origin-Resource-Policy", "cross-origin");

                // MANDATORY: Every document must have COOP/COEP.
                if (isSameOrigin && (
                    event.request.mode === "navigate" || 
                    response.headers.get("content-type")?.includes("text/html")
                )) {
                    newHeaders.set("Cross-Origin-Embedder-Policy", "require-corp");
                    newHeaders.set("Cross-Origin-Opener-Policy", "same-origin");
                }

                // Handle 304/204 specially: they MUST NOT have a body.
                // We create a new response with the injected headers.
                const isNoBody = response.status === 204 || response.status === 304;
                return new Response(isNoBody ? null : response.body, {
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
