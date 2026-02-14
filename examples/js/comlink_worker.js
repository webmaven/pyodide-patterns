importScripts("https://cdn.jsdelivr.net/npm/comlink/dist/umd/comlink.js");
importScripts("https://cdn.jsdelivr.net/pyodide/v0.28.0/full/pyodide.js");

class PyodideWorker {
    async init() {
        this.pyodide = await loadPyodide({
            indexURL: "https://cdn.jsdelivr.net/pyodide/v0.28.0/full/"
        });
        await this.pyodide.loadPackage("micropip");
        this.micropip = this.pyodide.pyimport("micropip");
    }

    async runPython(code) {
        if (!this.pyodide) {
            throw new Error("Pyodide not initialized. Call init() first.");
        }
        return await this.pyodide.runPythonAsync(code);
    }

    async installPackage(pkg) {
        await this.micropip.install(pkg);
    }
}

Comlink.expose(new PyodideWorker());
