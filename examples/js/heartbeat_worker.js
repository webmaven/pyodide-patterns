/**
 * Heartbeat Worker
 * A worker that responds to pings to prove it is still alive.
 */
importScripts("https://cdn.jsdelivr.net/pyodide/v0.28.0/full/pyodide.js");

self.onmessage = async (e) => {
    if (e.data.type === "PING") {
        // Respond immediately to pings
        self.postMessage({ type: "PONG", id: e.data.id });
        return;
    }

    if (e.data.type === "RUN") {
        try {
            if (!self.pyodide) {
                self.pyodide = await loadPyodide();
            }
            const result = await self.pyodide.runPythonAsync(e.data.code);
            self.postMessage({ type: "RESULT", result });
        } catch (err) {
            self.postMessage({ type: "ERROR", error: err.message });
        }
    }
    
    if (e.data.type === "CRASH_DEMO") {
        // Simulate a fatal crash by entering an infinite loop
        // that blocks the event loop, or just throwing an unhandled error.
        console.log("Worker: Simulating a silent crash (infinite loop)...");
        while(true) {} 
    }
};
