/**
 * Pyodide Loader Utility
 */

// Calculate project root from this script's own URL
const LOADER_URL = new URL(document.currentScript.src);
const PROJECT_ROOT = LOADER_URL.href.replace(/examples\/js\/pyodide_loader\.js$/, '');

window.loadPyodideAndFiles = async (files = []) => {
    console.log(`Loader: Initializing from ${PROJECT_ROOT}`);
    
    if (!window.crossOriginIsolated) {
        console.warn("Loader: Page is NOT cross-origin isolated. High-performance features (SAB, Threads) will fail.");
    }
    
    try { pyodide.FS.mkdir('pyodide_app'); } catch(e) {}
    pyodide.FS.writeFile('pyodide_app/__init__.py', '');
    try { pyodide.FS.mkdir('pyodide_app/bridge'); } catch(e) {}
    
    const prefix = `${PROJECT_ROOT}src/pyodide_app/`;

    const loadFile = async (url, dest) => {
        const resp = await fetch(url);
        if (!resp.ok) throw new Error(`Failed to fetch ${url}`);
        const text = await resp.text();
        pyodide.FS.writeFile(`pyodide_app/${dest}`, text);
    };

    // Load bridge
    await loadFile(`${prefix}bridge/__init__.py`, 'bridge/__init__.py');
    await loadFile(`${prefix}bridge/core.py`, 'bridge/core.py');
    await loadFile(`${prefix}bridge/reactivity.py`, 'bridge/reactivity.py');
    await loadFile(`${prefix}bridge/vdom.py`, 'bridge/vdom.py');

    // Load requested files
    for (const f of files) {
        await loadFile(`${prefix}${f}`, f);
    }

    return pyodide;
};
