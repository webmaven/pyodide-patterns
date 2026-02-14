/**
 * Pyodide Architecture - Isolation Guard
 * Ensures the page is Cross-Origin Isolated before Pyodide runs.
 */
(function() {
    // Dynamically calculate the path to the root service worker
    // based on this script's own location in /examples/js/
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
            if (window.crossOriginIsolated) {
                // Already isolated. Clean up the URL if needed.
                if (window.location.search.includes('coi=true')) {
                    const url = new URL(window.location.href);
                    url.searchParams.delete('coi');
                    window.history.replaceState({}, '', url.href);
                }
                return;
            }

            // If we aren't isolated, we need the SW to be active.
            if (reg.active) {
                // If it's active but we aren't isolated, and we haven't reloaded yet, do it now.
                if (!window.location.search.includes('coi=true')) {
                    reload();
                }
            } else {
                // Wait for the new worker to become active.
                reg.addEventListener("updatefound", () => {
                    const newWorker = reg.installing;
                    newWorker.addEventListener("statechange", () => {
                        if (newWorker.state === "activated" && !window.crossOriginIsolated) {
                            reload();
                        }
                    });
                });
            }
        }).catch(err => {
            console.error("Isolation Guard: Registration failed:", err);
        });
    }
})();
