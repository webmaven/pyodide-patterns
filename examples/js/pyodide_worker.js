// In the worker
self.importScripts("https://cdn.jsdelivr.net/pyodide/v0.28.0/full/pyodide.js");

async function runPyodide() {
    try {
        console.log("Worker: Loading Pyodide...");
        self.pyodide = await self.loadPyodide({ indexURL: "https://cdn.jsdelivr.net/pyodide/v0.28.0/full/" });
        console.log("Worker: Pyodide loaded.");

        // Run a simple Python script
        let result = await self.pyodide.runPythonAsync(`
            import sys
            sys.version
        `);

        self.postMessage({
            message: `Python script successful! Python version: ${result}`
        });

    } catch (error) {
        console.error("Worker: Pyodide initialization error:", error);
        self.postMessage({
            message: `Worker error: ${error.message}`
        });
    }
}

runPyodide();
