# Bootstrapping & Warm Starts

## Context
Pyodide applications suffer from a heavy "Cold Start" (often 10MB-20MB of initial downloads and several seconds of WASM compilation). This can lead to a poor user experience if they are greeted with a blank screen or a generic "Loading..." message for 10 seconds.

## Problem
How can we minimize user drop-off during the long initialization phase and provide the appearance of a fast, responsive application?

## Forces
*   **Asset Size**: Core WASM and standard library are large.
*   **Compilation Latency**: WASM bytecode must be compiled by the browser engine.
*   **Perceived vs. Actual Speed**: A 10-second load with a progress bar feels faster than a 5-second load with a blank screen.
*   **Bandwidth**: Users on mobile or poor connections may experience extremely long waits.

## Solution
Implement a **Multi-Stage Bootstrapping** strategy that combines technical caching with UX feedback patterns.

1.  **Immediate Background Start**: Start the `loadPyodide()` process as soon as the page begins to load, rather than waiting for user interaction or full UI rendering.
2.  **Progressive Milestones**: Break the initialization into user-facing milestones (e.g., "Downloading Runtime", "Initializing Python", "Preparing Packages").
3.  **Warm Starts (Caching)**: Use **Service Workers** (see Service Worker Caching pattern) to cache WASM assets locally, turning subsequent loads into "Warm Starts" that skip the download phase.
4.  **Optimistic UI**: Reveal portions of the UI that don't depend on Python logic immediately, while the background bootstrap completes.

## Implementation

### The Feedback Pattern
Use specific code hooks to update the UI at each stage of the Pyodide lifecycle.

```javascript
async function startApp() {
    updateUI("Downloading Pyodide...");
    const pyodide = await loadPyodide();
    
    updateUI("Initializing Python...");
    await pyodide.runPythonAsync("import sys");
    
    updateUI("Loading Data Science Tools...");
    await pyodide.loadPackage(["numpy", "pandas"]);
    
    revealApp();
}
```

### Background Bootstrapping
Avoid putting `loadPyodide` inside a "Click to Start" button unless absolutely necessary. Trigger it on `DOMContentLoaded`.

## Resulting Context
*   **Pros**: Significant reduction in user drop-off. Better professional polish.
*   **Cons**: Requires careful management of UI states (e.g., preventing user actions on buttons that require Python before it is ready).

## Related Patterns
*   **Service Worker Caching**: The technical foundation for "Warm Starts."
*   **Persistent File System (IDBFS)**: Used to persist user data during the "Warm Start."
*   **Worker RPC**: Moving the bootstrap into a worker to prevent UI thread "hiccups" during compilation.

## Verification
*   **Example**: `examples/loading/progressive_bootstrapping.html`
*   **Test**: `tests/patterns/loading/test_bootstrapping.py`
