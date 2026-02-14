// A simple worker pool for Pyodide using Comlink
class PyodidePool {
    constructor(workerUrl, size = navigator.hardwareConcurrency || 2) {
        this.workerUrl = workerUrl;
        this.size = size;
        this.workers = []; // Array of { proxy, busy: boolean }
        this.queue = [];
    }

    async init() {
        console.log(`Initializing Pyodide Pool with ${this.size} workers...`);
        const initPromises = [];
        
        for (let i = 0; i < this.size; i++) {
            const worker = new Worker(this.workerUrl);
            const proxy = Comlink.wrap(worker);
            const workerObj = { proxy, busy: false, id: i };
            this.workers.push(workerObj);
            
            // Start initialization immediately in parallel
            initPromises.push(proxy.init());
        }
        
        await Promise.all(initPromises);
        console.log("Pyodide Pool Ready.");
    }

    async run(code) {
        return new Promise((resolve, reject) => {
            const task = { code, resolve, reject };
            this.queue.push(task);
            this._processQueue();
        });
    }

    _processQueue() {
        if (this.queue.length === 0) return;

        // Find an available worker
        const availableWorker = this.workers.find(w => !w.busy);
        if (!availableWorker) return;

        const task = this.queue.shift();
        availableWorker.busy = true;

        console.log(`Worker ${availableWorker.id} starting task...`);
        
        availableWorker.proxy.runPython(task.code)
            .then(result => {
                availableWorker.busy = false;
                task.resolve(result);
                this._processQueue(); // Check for more tasks
            })
            .catch(err => {
                availableWorker.busy = false;
                task.reject(err);
                this._processQueue();
            });
    }
}

// Export for use in HTML
window.PyodidePool = PyodidePool;
