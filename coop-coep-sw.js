/*
 * High-Visibility COOP/COEP Service Worker
 * Version: 2.1.0
 */

const DEBUG = true;
const log = (...args) => DEBUG && console.log("[SW]", ...args);

self.addEventListener("install", () => {
    log("Installing...");
    self.skipWaiting();
});

self.addEventListener("activate", (event) => {
    log("Activating and claiming clients...");
    event.waitUntil(self.clients.claim());
});

self.addEventListener("fetch", (event) => {
    const url = new URL(event.request.url);
    const isSameOrigin = url.origin === self.location.origin;

    // We only care about GET requests for isolation
    if (event.request.method !== "GET") return;

    // Skip non-interesting extensions
    if (url.pathname.endsWith(".png") || url.pathname.endsWith(".ico")) return;

    event.respondWith(
        fetch(isSameOrigin ? event.request : new Request(event.request, { mode: "cors" }))
            .then((response) => {
                if (!response) return response;
                
                // If it's a 304 or similar, we can't easily wrap it, but we should try
                if (response.status === 0) {
                    log("Opaque response encountered:", url.href);
                    return response;
                }

                const newHeaders = new Headers(response.headers);
                
                // Set CORP to cross-origin for EVERYTHING to be safe
                newHeaders.set("Cross-Origin-Resource-Policy", "cross-origin");

                if (isSameOrigin && (
                    event.request.mode === "navigate" || 
                    response.headers.get("content-type")?.includes("text/html")
                )) {
                    log("Injecting isolation headers for navigation:", url.pathname);
                    newHeaders.set("Cross-Origin-Embedder-Policy", "require-corp");
                    newHeaders.set("Cross-Origin-Opener-Policy", "same-origin");
                }

                // Handle no-body responses (304, etc)
                const body = (response.status === 204 || response.status === 304) 
                    ? null 
                    : response.body;

                return new Response(body, {
                    status: response.status,
                    statusText: response.statusText,
                    headers: newHeaders,
                });
            })
            .catch((err) => {
                log("Fetch error for", url.href, err);
                return fetch(event.request);
            })
    );
});
