/**
 * Pyodide Loader Utility
 * Synchronizes the local Python source files into the Pyodide virtual filesystem
 * to enable standard imports.
 */

// Get the base URL of this loader script to resolve relative paths correctly
const LOADER_BASE_URL = new URL(document.currentScript.src).href.replace(/js\/pyodide_loader\.js$/, '');

window.loadPyodideAndFiles = async (files = [], srcPrefix = null) => {
    // If no prefix is provided, we assume src is sibling to the loader's parent dir
    // e.g. /examples/js/pyodide_loader.js -> /src/pyodide_app/
    const defaultSrcPrefix = LOADER_BASE_URL + '../src/pyodide_app/';
    const prefix = srcPrefix || defaultSrcPrefix;

    const pyodide = await loadPyodide();
    
    // Create package directory
    try { pyodide.FS.mkdir('pyodide_app'); } catch(e) {}
    // Create __init__.py to make it a package
    pyodide.FS.writeFile('pyodide_app/__init__.py', '');
    
    // Create bridge directory
    try { pyodide.FS.mkdir('pyodide_app/bridge'); } catch(e) {}
    
    const loadFile = async (url, dest) => {
        console.log(`Loader: Fetching ${url} -> pyodide_app/${dest}`);
        const resp = await fetch(url);
        if (!resp.ok) throw new Error(`Failed to fetch ${url} (Status: ${resp.status})`);
        const text = await resp.text();
        pyodide.FS.writeFile(`pyodide_app/${dest}`, text);
    };

    // Always load the bridge module files
    await loadFile(`${prefix}bridge/__init__.py`, 'bridge/__init__.py');
    await loadFile(`${prefix}bridge/core.py`, 'bridge/core.py');
    await loadFile(`${prefix}bridge/reactivity.py`, 'bridge/reactivity.py');
    await loadFile(`${prefix}bridge/vdom.py`, 'bridge/vdom.py');

    for (const f of files) {
        await loadFile(`${prefix}${f}`, f);
    }

    return pyodide;
};
