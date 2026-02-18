window.spawnIsolatedWorker = async (workerCode) => {
    const comlinkCode = await (await fetch(new URL('../vendor/comlink.js', import.meta.url))).text();
    const pyodideCode = await (await fetch(new URL('../vendor/pyodide.js', import.meta.url))).text();
    
    const blobCode = `
        ${comlinkCode}
        ${pyodideCode}
        ${workerCode}
    `;
    const blob = new Blob([blobCode], { type: 'application/javascript' });
    return new Worker(URL.createObjectURL(blob));
};
