/**
 * Pyodide Architecture - Manual Shield Worker Hub
 * Version: 3.0.0
 * Uses Fetch+Eval to ensure SW header injection is respected.
 */
(async function() {
    try {
        const log = (...args) => console.log(`[Worker Hub v3.0.0]`, ...args);
        
        async function loadScript(url) {
            log(`Fetching dependency: ${url}`);
            const resp = await fetch(url);
            if (!resp.ok) throw new Error(`Failed to fetch ${url}`);
            const code = await resp.text();
            // Eval the code in the global worker scope
            (0, eval)(code);
        }

        // Use absolute paths relative to root
        await loadScript("./examples/vendor/comlink.js");
        await loadScript("./examples/vendor/pyodide.js");

        class PyodideWorker {
            async init() {
                this.pyodide = await loadPyodide({
                    indexURL: "./examples/vendor/"
                });
            }
            async runPython(code) {
                return await this.pyodide.runPythonAsync(code);
            }
        }

        Comlink.expose(new PyodideWorker());
        log("Hub ready and exposed.");
    } catch (e) {
        console.error("FATAL Hub Error:", e);
        self.postMessage({ type: 'error', message: e.message });
    }
})();
