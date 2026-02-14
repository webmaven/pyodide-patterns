/**
 * COOP/COEP Service Worker Registration Guard
 * Ensures the page is Cross-Origin Isolated before Pyodide runs.
 */
(function() {
    // Path to the service worker at the project root
    const swPath = window.location.pathname.includes('/examples/') 
        ? '../../coop-coep-sw.js' 
        : 'coop-coep-sw.js';

    if ("serviceWorker" in navigator) {
        navigator.serviceWorker.register(swPath).then(reg => {
            // If the page isn't isolated yet, we need a refresh to 
            // let the Service Worker intercept the next document request.
            if (!window.crossOriginIsolated && !window.location.search.includes('sw-fixed=true')) {
                console.log("Page is not isolated. Reloading to apply SW headers...");
                const url = new URL(window.location.href);
                url.searchParams.set('sw-fixed', 'true');
                window.location.href = url.href;
            }
        });
    }
})();
