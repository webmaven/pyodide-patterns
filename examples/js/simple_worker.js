// This worker does nothing but listen for messages.
// It doesn't need Pyodide. Its only purpose is to be a target
// for the main thread to post a message to.

self.onmessage = (event) => {
    // We don't expect this to ever be called in the DataCloneError test.
    console.log("Simple worker received:", event.data);
};
