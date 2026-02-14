/**
 * Pyodide Architecture - Isolation Guard
 * Ensures the page is Cross-Origin Isolated before Pyodide runs.
 */
(function() {
    // Dynamically calculate the path to the root service worker
    // based on this script's own location in /examples/js/
    const scriptUrl = new URL(document.currentScript.src);
    const swPath = scriptUrl.href.replace(/examples\/js\/sw_registration\.js$/, 'coop-coep-sw.js');

    if ("serviceWorker" in navigator) {
        navigator.serviceWorker.register(swPath).then(reg => {
            // Check if we need to reload to enable isolation.
            // We only reload if:
            // 1. We aren't isolated yet.
            // 2. The SW is ready (active).
            // 3. We haven't already reloaded (to prevent loops).
            if (!window.crossOriginIsolated && reg.active && !window.location.search.includes('sw-fixed=true')) {
                console.log("Isolation Guard: Re-establishing shield...");
                const url = new URL(window.location.href);
                url.searchParams.set('sw-fixed', 'true');
                window.location.href = url.href;
            }
        }).catch(err => {
            console.error("Isolation Guard: Registration failed:", err);
        });
    }
})();
