const CACHE_NAME = 'pyodide-v1';
const ASSETS_TO_CACHE = [
    'https://cdn.jsdelivr.net/pyodide/v0.28.0/full/pyodide.js',
    'https://cdn.jsdelivr.net/pyodide/v0.28.0/full/pyodide.asm.js',
    'https://cdn.jsdelivr.net/pyodide/v0.28.0/full/pyodide.asm.wasm',
    'https://cdn.jsdelivr.net/pyodide/v0.28.0/full/python_stdlib.zip'
];

self.addEventListener('install', (event) => {
    self.skipWaiting();
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
    // Only cache GET requests for the Pyodide CDN
    if (event.request.method === 'GET' && event.request.url.includes('cdn.jsdelivr.net')) {
        event.respondWith(
            caches.match(event.request).then((response) => {
                return response || fetch(event.request).then((fetchResponse) => {
                    return caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, fetchResponse.clone());
                        return fetchResponse;
                    });
                });
            })
        );
    }
});
