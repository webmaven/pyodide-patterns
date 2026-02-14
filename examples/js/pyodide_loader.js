/**
 * Pyodide Loader Utility
 * Synchronizes the local Python source files into the Pyodide virtual filesystem
 * to enable standard imports.
 */

// Get the base URL of the project root
// If script is at /examples/js/pyodide_loader.js, root is /
const SCRIPT_URL = new URL(document.currentScript.src);
const PROJECT_ROOT = SCRIPT_URL.href.replace(/examples\/js\/pyodide_loader\.js$/, '');

window.loadPyodideAndFiles = async (files = []) => {
    console.log(`Loader: Project Root detected as: ${PROJECT_ROOT}`);
    const prefix = PROJECT_ROOT + 'src/pyodide_app/';

    const pyodide = await loadPyodide();
    
    // Create package directory
    try { pyodide.FS.mkdir('pyodide_app'); } catch(e) {}
    // Create __init__.py to make it a package
    pyodide.FS.writeFile('pyodide_app/__init__.py', '');
    
    // Create bridge directory
    try { pyodide.FS.mkdir('pyodide_app/bridge'); } catch(e) {}
    
    const loadFile = async (url, dest) => {
        console.log(`Loader: Fetching ${url} -> pyodide_app/${dest}`);
        try {
            const resp = await fetch(url);
            if (!resp.ok) {
                console.error(`Loader: 404 for ${url}`);
                throw new Error(`Failed to fetch ${url} (Status: ${resp.status})`);
            }
            const text = await resp.text();
            pyodide.FS.writeFile(`pyodide_app/${dest}`, text);
        } catch (err) {
            console.error(`Loader: Fatal error fetching ${url}:`, err);
            throw err;
        }
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
