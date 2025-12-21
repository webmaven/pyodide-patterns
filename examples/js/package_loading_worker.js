// In the worker
self.importScripts("https://cdn.jsdelivr.net/pyodide/v0.28.0/full/pyodide.js");

async function initializePyodide() {
    try {
        postMessage({ type: "status", message: "Loading Pyodide..." });
        self.pyodide = await self.loadPyodide();
        await self.pyodide.loadPackage("micropip");
        self.micropip = self.pyodide.pyimport("micropip");
        postMessage({ type: "status", message: "Pyodide and micropip ready." });
    } catch (error) {
        postMessage({ type: "error", message: `Pyodide init failed: ${error}` });
    }
}

const pyodideReadyPromise = initializePyodide();

self.onmessage = async (event) => {
    await pyodideReadyPromise;
    const { pkgName } = event.data;

    try {
        postMessage({ type: "status", message: `Installing '${pkgName}'...` });
        await self.micropip.install(pkgName);
        postMessage({ type: "status", message: `'${pkgName}' installed successfully.` });

        // Verify by importing
        self.pyodide.pyimport(pkgName);
        postMessage({ type: "success", pkgName: pkgName });

    } catch (error) {
        console.error(`Worker failed to install '${pkgName}':`, error);
        postMessage({ type: "error", message: error.message });
    }
};
