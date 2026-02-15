/**
 * Pyodide Comlink Worker
 */
console.log(`[${new Date().toISOString()}] Worker: Script execution started.`);

try {
    importScripts("https://cdn.jsdelivr.net/npm/comlink/dist/umd/comlink.js");
    console.log(`[${new Date().toISOString()}] Worker: Comlink imported.`);
    
    importScripts("https://cdn.jsdelivr.net/pyodide/v0.28.0/full/pyodide.js");
    console.log(`[${new Date().toISOString()}] Worker: Pyodide script imported.`);
} catch (e) {
    console.error(`[${new Date().toISOString()}] Worker: Failed to import scripts:`, e);
}

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
