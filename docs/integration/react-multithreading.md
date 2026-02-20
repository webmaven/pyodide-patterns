# Integration Recipe: React + Multithreading

How to use the Atomic Worker Shield within a React functional component.

## 1. Setup Service Worker
Register the `coop-coep-sw.js` in your entry point (e.g., `index.js`).

## 2. The Hook
Create a custom hook to manage the isolated worker lifecycle.

```javascript
import { useEffect, useState } from 'react';

export function usePyodideWorker() {
  const [worker, setWorker] = useState(null);

  useEffect(() => {
    async function setup() {
      // 1. Wait for isolation shield
      if (!(await window.waitForShield())) return;

      // 2. Define worker logic
      const logic = `
        importScripts('./vendor/pyodide.js');
        // ... worker implementation
      `;

      // 3. Spawn via Atomic Shield
      const w = await window.spawnIsolatedWorker(logic);
      setWorker(w);
    }
    setup();
  }, []);

  return worker;
}
```

## 3. Usage in Component
```javascript
function heavyComponent() {
  const worker = usePyodideWorker();
  
  const runMath = async () => {
    const result = await worker.runPython("1 + 1");
    console.log(result);
  };

  return <button onClick={runMath} disabled={!worker}>Run</button>;
}
```
