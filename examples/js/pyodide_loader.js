/**
 * Pyodide Loader Utility
 * Synchronizes the local Python source files into the Pyodide virtual filesystem
 * to enable standard imports.
 */
window.loadPyodideAndFiles = async (files = []) => {
    const pyodide = await loadPyodide();
    
    // Create package directory
    try { pyodide.FS.mkdir('pyodide_app'); } catch(e) {}
    // Create __init__.py to make it a package
    pyodide.FS.writeFile('pyodide_app/__init__.py', '');
    
    const loadFile = async (url, dest) => {
        const resp = await fetch(url);
        if (!resp.ok) throw new Error(`Failed to fetch ${url}`);
        const text = await resp.text();
        pyodide.FS.writeFile(`pyodide_app/${dest}`, text);
    };

    // Always load the bridge
    await loadFile('../../src/pyodide_app/bridge.py', 'bridge.py');

    for (const f of files) {
        await loadFile(`../../src/pyodide_app/${f}`, f);
    }

    return pyodide;
};
