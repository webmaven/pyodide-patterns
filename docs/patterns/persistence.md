# Persistent File System (IDBFS)

## Context
By default, the Pyodide file system is stored in WASM memory. When the page is refreshed or closed, all files written to the virtual file system are lost. For applications that handle user documents, configurations, or local databases, data must persist across sessions.

## Problem
How can we ensure that files written via standard Python I/O (`open()`, `os.write()`) are saved to the user's browser and restored automatically when the application restarts?

## Forces
*   **WASM Ephemerality**: Memory-backed file systems do not survive a reload.
*   **Asynchronous Storage**: IndexedDB (the browser's storage) is asynchronous, while standard Python file I/O is synchronous.
*   **Manual Syncing**: Emscripten's `IDBFS` requires manual synchronization calls to move data between the in-memory WASM heap and the browser's persistent store.

## Solution
Mount a specific directory to **`IDBFS`** (IndexedDB File System) and use **`syncfs`** to manage data persistence.

1.  **Mount**: Use `pyodide.FS.mount(pyodide.FS.filesystems.IDBFS, {}, '/your-dir')`.
2.  **Initial Sync (Load)**: Call `pyodide.FS.syncfs(true, callback)` during initialization to fetch existing data from IndexedDB into memory.
3.  **Standard I/O**: Use standard Python `with open('/your-dir/file.txt', 'w')` to read/write.
4.  **Final Sync (Save)**: Call `pyodide.FS.syncfs(false, callback)` after writes to flush the memory changes back to IndexedDB.

## Implementation

### The Persistence Bridge
```javascript
// Initialization
pyodide.FS.mkdir('/data');
pyodide.FS.mount(pyodide.FS.filesystems.IDBFS, {}, '/data');

// Sync from persistent storage to memory on startup
await new Promise((resolve, reject) => {
    pyodide.FS.syncfs(true, (err) => err ? reject(err) : resolve());
});

// Writing data (Python)
pyodide.runPython("open('/data/config.json', 'w').write('{}')");

// Flush to disk
await new Promise((resolve, reject) => {
    pyodide.FS.syncfs(false, (err) => err ? reject(err) : resolve());
});
```

## Resulting Context
*   **Pros**: Standard Python libraries (like `sqlite3` or `pandas`) can use the persistent folder naturally. Data survives page reloads and browser restarts.
*   **Cons**: Synchronization is manual. If the browser crashes *after* a write but *before* a `syncfs(false)` call, the data will be lost.

## Related Patterns
*   **UX Bootstrapping**: Syncing large amounts of data from IndexedDB can add to the perceived startup time.
*   **Memory Management**: Be mindful of the WASM heap size when loading large files from `IDBFS`.

## Verification
*   **Example**: `examples/loading/persistence.html`
*   **Test**: `tests/patterns/loading/test_persistence.py`
