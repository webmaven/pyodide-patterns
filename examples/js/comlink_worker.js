/**
 * Pyodide Comlink Worker
 * Version: 2.5.0 (Pure Origin)
 */
(function() {
    const VERSION = "2.5.0";
    const log = (...args) => console.log(`[${new Date().toISOString()}] [Worker v${VERSION}]`, ...args);

    try {
        log("Starting script load...");
        
        // Use vendored same-origin scripts
        importScripts("../vendor/comlink.js");
        importScripts("../vendor/pyodide.js");
        
        log("Scripts imported.");

        class PyodideWorker {
            async init() {
                log("init() called.");
                try {
                    // Use vendored same-origin runtime
                    this.pyodide = await loadPyodide({
                        indexURL: "../vendor/"
                    });
                    log("loadPyodide() complete.");
                    
                    // We don't load micropip by default to keep it lightweight
                    // unless specifically needed by a demo.
                } catch (err) {
                    console.error(`[Worker v${VERSION}] init() failed:`, err);
                    throw err;
                }
            }

            async runPython(code) {
                return await this.pyodide.runPythonAsync(code);
            }
        }

        Comlink.expose(new PyodideWorker());
        log("Comlink exposed.");

    } catch (e) {
        console.error(`[Worker v${VERSION}] FATAL Error:`, e);
        self.postMessage({ type: 'error', message: e.message });
    }
})();
