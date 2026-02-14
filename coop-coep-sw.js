/*
 * COOP/COEP Service Worker Workaround for GitHub Pages
 * Derived from: https://github.com/gzuidhof/coi-serviceworker
 */

if (typeof window === "undefined") {
    self.addEventListener("install", () => self.skipWaiting());
    self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

    self.addEventListener("fetch", (event) => {
        const requestUrl = new URL(event.request.url);
        
        // Only intercept requests to our own origin or those within our project path
        // On GitHub Pages, the origin is https://webmaven.github.io
        // but the path is /pyodide-patterns/
        const isSameOrigin = requestUrl.origin === self.location.origin;
        
        if (!isSameOrigin) {
            return;
        }

        if (event.request.cache === "only-if-cached" && event.request.mode !== "same-origin") {
            return;
        }

        event.respondWith(
            fetch(event.request)
                .then((response) => {
                    if (response.status === 0) {
                        return response;
                    }

                    const newHeaders = new Headers(response.headers);
                    newHeaders.set("Cross-Origin-Embedder-Policy", "require-corp");
                    newHeaders.set("Cross-Origin-Opener-Policy", "same-origin");
                    newHeaders.set("Cross-Origin-Resource-Policy", "cross-origin");

                    return new Response(response.body, {
                        status: response.status,
                        statusText: response.statusText,
                        headers: newHeaders,
                    });
                })
                .catch((e) => console.error("SW Fetch Error:", e))
        );
    });
}
