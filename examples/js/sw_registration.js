/**
 * Pyodide Architecture - Isolation Guard
 * Version: 2.3.6 (Stable Isolation)
 */
(function() {
    const VERSION = "2.3.6";
    const scriptUrl = new URL(document.currentScript.src);
    
    // Robustly find project root by splitting at the known script path
    const projectRoot = scriptUrl.href.split('examples/js/sw_registration.js')[0];
    const swPath = `${projectRoot}coop-coep-sw.js?v=${Date.now()}`;

    console.log(`[${new Date().toISOString()}] [ISO Guard v${VERSION}] Starting...`);
    console.log(`[${new Date().toISOString()}] [ISO Guard v${VERSION}] Project Root: ${projectRoot}`);

    function reload() {
        console.log(`[${new Date().toISOString()}] [ISO Guard v${VERSION}] Reloading to activate shield...`);
        const url = new URL(window.location.href);
        url.searchParams.set('coi', 'true');
        window.location.href = url.href;
    }

    if ("serviceWorker" in navigator) {
        // Register with explicit scope to ensure it covers the entire project
        navigator.serviceWorker.register(swPath, { scope: projectRoot }).then(reg => {
            console.log(`[${new Date().toISOString()}] [ISO Guard v${VERSION}] SW status:`, {
                active: !!reg.active,
                controlling: !!navigator.serviceWorker.controller,
                isolated: window.crossOriginIsolated,
                scope: reg.scope
            });
            
            if (window.crossOriginIsolated) {
                if (window.location.search.includes('coi=true')) {
                    const url = new URL(window.location.href);
                    url.searchParams.delete('coi');
                    window.history.replaceState({}, '', url.href);
                }
                return;
            }

            // If SW is active but we aren't isolated, we need a refresh
            if (reg.active && !window.location.search.includes('coi=true')) {
                reload();
            }

            reg.addEventListener("updatefound", () => {
                const newWorker = reg.installing;
                newWorker.addEventListener("statechange", () => {
                    if (newWorker.state === "activated" && !window.crossOriginIsolated) {
                        reload();
                    }
                });
            });
        }).catch(err => {
            console.error(`[${new Date().toISOString()}] [ISO Guard v${VERSION}] Registration failed:`, err);
        });
    }
})();
