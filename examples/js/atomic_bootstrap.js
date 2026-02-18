/**
 * Pyodide Architecture - Atomic Bootstrapper
 * Version: 6.0.1
 * Spawns an isolated worker by inlining dependencies into a Blob.
 */
(function() {
    // Calculate paths relative to this script
    const scriptUrl = new URL(document.currentScript.src);
    const vendorPath = new URL('../vendor/', scriptUrl).href;

    window.spawnIsolatedWorker = async (workerCode) => {
        console.log(`[ISO Atomic] Fetching dependencies from: ${vendorPath}`);
        
        // Fetch dependencies as text
        const [comlinkCode, pyodideCode] = await Promise.all([
            fetch(`${vendorPath}comlink.js`).then(r => r.text()),
            fetch(`${vendorPath}pyodide.js`).then(r => r.text())
        ]);
        
        // Combine into a single source
        const blobCode = `
            ${comlinkCode}
            ${pyodideCode}
            ${workerCode}
        `;
        
        const blob = new Blob([blobCode], { type: 'application/javascript' });
        const workerUrl = URL.createObjectURL(blob);
        
        console.log(`[ISO Atomic] Spawning worker from Blob URL.`);
        return new Worker(workerUrl);
    };
    
    console.log(`[ISO Atomic] v6.0.1 utility ready.`);
})();
