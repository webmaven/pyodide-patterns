/**
 * Atomic Worker Shield - Self-Contained Snippet
 * 
 * Usage:
 * const worker = await spawnIsolatedWorker(`
 *   self.onmessage = (e) => self.postMessage('pong');
 * `);
 */
async function spawnIsolatedWorker(workerCode, vendorPath = './vendor/') {
    const deps = ['comlink.js', 'pyodide.js'];
    const codes = await Promise.all(
        deps.map(d => fetch(vendorPath + d).then(r => r.text()))
    );
    
    const blobCode = `
        ${codes.join('
')}
        ${workerCode}
    `;
    
    const blob = new Blob([blobCode], { type: 'application/javascript' });
    return new Worker(URL.createObjectURL(blob));
}
