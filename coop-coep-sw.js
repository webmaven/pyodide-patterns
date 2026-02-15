/*
 * Definitive COOP/COEP/CORP Service Worker
 * This version uses the 'Proxy-Fetch' pattern to ensure all resources
 * (including external CDNs) are served with the headers required for isolation.
 */

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") return;

    const url = new URL(event.request.url);
    const isSameOrigin = url.origin === self.location.origin;

    // We only proxy requests that might be blocked by COEP:
    // 1. Same-origin (to inject COOP/COEP/CORP)
    // 2. Cross-origin (to inject CORP if the CDN doesn't)
    
    event.respondWith(
        fetch(event.request, {
            // If cross-origin, we MUST use 'cors' mode to be able to read/modify headers
            mode: isSameOrigin ? event.request.mode : "cors",
            credentials: isSameOrigin ? "include" : "omit",
            redirect: "follow"
        }).then((response) => {
            if (!response) return response;
            
            // If the response is opaque (no CORS), we can't do anything.
            // But since we requested with mode: 'cors', it shouldn't be opaque 
            // if the CDN supports CORS (which JSDelivr does).
            if (response.status === 0) return response;

            const newHeaders = new Headers(response.headers);
            
            // 1. Always provide CORP: cross-origin to satisfy the browser
            newHeaders.set("Cross-Origin-Resource-Policy", "cross-origin");

            // 2. If it's a same-origin navigation, inject the master isolation headers
            if (isSameOrigin && (
                event.request.mode === "navigate" || 
                response.headers.get("content-type")?.includes("text/html")
            )) {
                newHeaders.set("Cross-Origin-Embedder-Policy", "require-corp");
                newHeaders.set("Cross-Origin-Opener-Policy", "same-origin");
                // Cache-busting for navigation
                newHeaders.set("Cache-Control", "no-cache, no-store, must-revalidate");
            }

            return new Response(response.body, {
                status: response.status,
                statusText: response.statusText,
                headers: newHeaders,
            });
        }).catch(err => {
            console.error("SW Proxy Error:", url.href, err);
            // Fallback to original request if proxying fails
            return fetch(event.request);
        })
    );
});
