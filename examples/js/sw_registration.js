/**
 * Pyodide Architecture - Isolation Guard
 * Ensures the page is Cross-Origin Isolated before Pyodide runs.
 */
(function() {
    const scriptUrl = new URL(document.currentScript.src);
    const swPath = scriptUrl.href.replace(/examples\/js\/sw_registration\.js$/, 'coop-coep-sw.js');

    function reload() {
        console.log("Isolation Guard: Reloading to activate shield...");
        const url = new URL(window.location.href);
        url.searchParams.set('coi', 'true');
        window.location.href = url.href;
    }

    if ("serviceWorker" in navigator) {
        navigator.serviceWorker.register(swPath).then(reg => {
            console.log("Isolation Guard: SW registered. Active:", !!reg.active, "Isolated:", window.crossOriginIsolated);
            
            if (window.crossOriginIsolated) {
                // Already isolated. Clean up the URL.
                if (window.location.search.includes('coi=true')) {
                    const url = new URL(window.location.href);
                    url.searchParams.delete('coi');
                    window.history.replaceState({}, '', url.href);
                }
                return;
            }

            // Force reload if we have an active worker but no isolation
            if (reg.active && !window.location.search.includes('coi=true')) {
                reload();
            }

            // Handle new worker activation
            reg.addEventListener("updatefound", () => {
                const newWorker = reg.installing;
                newWorker.addEventListener("statechange", () => {
                    if (newWorker.state === "activated" && !window.crossOriginIsolated) {
                        reload();
                    }
                });
            });
        });

        navigator.serviceWorker.addEventListener("controllerchange", () => {
            if (!window.crossOriginIsolated) reload();
        });
    }
})();
