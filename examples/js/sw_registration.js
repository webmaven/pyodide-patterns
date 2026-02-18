/**
 * Pyodide Architecture - Isolation Guard
 * Version: 6.0.0 (Atomic Shield)
 */
(function() {
    const VERSION = "6.0.0";
    const scriptUrl = new URL(document.currentScript.src);
    const projectRoot = scriptUrl.href.split('examples/js/sw_registration.js')[0];
    const swPath = `${projectRoot}coop-coep-sw.js?v=${VERSION}`;

    console.log(`[${new Date().toISOString()}] [ISO Guard v${VERSION}] Starting...`);

    window.waitForShield = async () => {
        if (!navigator.serviceWorker) return false;
        const pingUrl = `${projectRoot}__ping__`;
        for (let i = 0; i < 20; i++) {
            try {
                const resp = await fetch(pingUrl);
                if (resp.ok && (await resp.text()) === "pong") return true;
            } catch (e) {}
            await new Promise(r => setTimeout(r, 250));
        }
        return false;
    };

    function reload() {
        const url = new URL(window.location.href);
        url.searchParams.set('coi', 'true');
        window.location.href = url.href;
    }

    if ("serviceWorker" in navigator) {
        navigator.serviceWorker.register(swPath, { scope: projectRoot }).then(reg => {
            console.log(`[${new Date().toISOString()}] [ISO Guard v${VERSION}] SW status:`, {
                active: !!reg.active,
                controlling: !!navigator.serviceWorker.controller,
                isolated: window.crossOriginIsolated
            });
            
            if (window.crossOriginIsolated && navigator.serviceWorker.controller) {
                if (window.location.search.includes('coi=true')) {
                    const url = new URL(window.location.href);
                    url.searchParams.delete('coi');
                    window.history.replaceState({}, '', url.href);
                }
                return;
            }

            if (reg.active && !window.location.search.includes('coi=true')) reload();
            
            reg.addEventListener("updatefound", () => {
                const newWorker = reg.installing;
                newWorker.addEventListener("statechange", () => {
                    if (newWorker.state === "activated" && !window.crossOriginIsolated) reload();
                });
            });
        });
    }
})();
