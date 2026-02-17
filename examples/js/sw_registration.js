/**
 * Pyodide Architecture - Isolation Guard
 * Version: 2.3.3 (Stable Isolation)
 */
(function() {
    const VERSION = "2.3.3";
    const scriptUrl = new URL(document.currentScript.src);
    // Add cache-busting to the SW registration itself
    const swPath = scriptUrl.href.replace(/examples\/js\/sw_registration\.js$/, `coop-coep-sw.js?v=${Date.now()}`);

    console.log(`[${new Date().toISOString()}] Isolation Guard v${VERSION} starting...`);
    console.log(`[${new Date().toISOString()}] Isolation Guard: Source: ${scriptUrl.href}`);

    function reload() {
        console.log(`[${new Date().toISOString()}] Isolation Guard: Reloading to activate shield...`);
        const url = new URL(window.location.href);
        url.searchParams.set('coi', 'true');
        window.location.href = url.href;
    }

    if ("serviceWorker" in navigator) {
        navigator.serviceWorker.register(swPath).then(reg => {
            console.log(`[${new Date().toISOString()}] Isolation Guard: SW status -`, {
                active: !!reg.active,
                controlling: !!navigator.serviceWorker.controller,
                isolated: window.crossOriginIsolated
            });
            
            if (window.crossOriginIsolated) {
                if (window.location.search.includes('coi=true')) {
                    const url = new URL(window.location.href);
                    url.searchParams.delete('coi');
                    window.history.replaceState({}, '', url.href);
                }
                return;
            }

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
        });

        navigator.serviceWorker.addEventListener("controllerchange", () => {
            if (!window.crossOriginIsolated) reload();
        });
    }
})();
