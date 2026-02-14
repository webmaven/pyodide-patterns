/**
 * Pyodide Architecture - Isolation Guard
 * Ensures the page is Cross-Origin Isolated before Pyodide runs.
 */
(function() {
    // Calculate path to root SW
    const depth = (window.location.pathname.match(/\//g) || []).length;
    // For repo at /pyodide-patterns/, depth 1 is root, depth 2 is examples/
    const isRoot = !window.location.pathname.includes('/examples/');
    const swPath = isRoot ? './coop-coep-sw.js' : '../../coop-coep-sw.js';

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
        });
    }
})();
