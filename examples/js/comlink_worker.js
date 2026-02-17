/**
 * Pyodide Comlink Worker
 */
(function() {
    try {
        console.log(`[${new Date().toISOString()}] Worker: Starting script load...`);
        
        // Wrap everything in a closure to catch early errors
        importScripts("https://cdn.jsdelivr.net/npm/comlink/dist/umd/comlink.js");
        importScripts("https://cdn.jsdelivr.net/pyodide/v0.28.0/full/pyodide.js");
        
        console.log(`[${new Date().toISOString()}] Worker: Scripts imported.`);

        class PyodideWorker {
            async init() {
                console.log(`[${new Date().toISOString()}] Worker: init() called.`);
                try {
                    this.pyodide = await loadPyodide({
                        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.28.0/full/"
                    });
                    console.log(`[${new Date().toISOString()}] Worker: loadPyodide() complete.`);
                    
                    await this.pyodide.loadPackage("micropip");
                    this.micropip = this.pyodide.pyimport("micropip");
                    console.log(`[${new Date().toISOString()}] Worker: Micropip ready.`);
                } catch (err) {
                    console.error(`[${new Date().toISOString()}] Worker: init() failed:`, err);
                    throw err;
                }
            }

            async runPython(code) {
                return await this.pyodide.runPythonAsync(code);
            }
        }

        Comlink.expose(new PyodideWorker());
        console.log(`[${new Date().toISOString()}] Worker: Comlink exposed.`);

    } catch (e) {
        console.error(`[${new Date().toISOString()}] FATAL Error in worker script:`, e);
        // Attempt to send the error back to the main thread
        self.postMessage({ type: 'error', message: e.message, stack: e.stack });
    }
})();
