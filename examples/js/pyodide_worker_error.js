// In the worker
self.importScripts("https://cdn.jsdelivr.net/pyodide/v0.28.0/full/pyodide.js");

async function runPyodide() {
    try {
        self.pyodide = await self.loadPyodide({ indexURL: "https://cdn.jsdelivr.net/pyodide/v0.28.0/full/" });

        // Run a Python script that will cause an error
        await self.pyodide.runPythonAsync(`
            print("About to cause a ZeroDivisionError in the worker...")
            x = 1 / 0
        `);

        self.postMessage({
            message: "This should not appear!"
        });

    } catch (error) {
        console.error("Worker: Caught a Python error:", error.message);
        // This is the key part: we send the error back to the main thread.
        self.postMessage({
            message: `Worker caught Python error: ${error.message}`
        });
    }
}

runPyodide();
