# WebGPU Compute Acceleration

## Context
Pyodide applications often involve heavy numerical computations (e.g., image processing, simulation, machine learning). While NumPy and SciPy provide optimized C extensions, the execution still happens on the CPU. For highly parallelizable tasks, the **WebGPU API** allows Python code to leverage the machine's GPU directly from the browser.

## Problem
Python is a high-level language with significant overhead for fine-grained parallel loops. Directly bridging Python logic to GPU kernels requires handling low-level buffer management, synchronization, and data marshaling between the WASM heap and GPU memory.

## Forces
*   **Parallelism**: GPUs can handle thousands of concurrent operations, whereas WASM is largely single-threaded (until pthreads are enabled).
*   **Data Transfer**: Moving data from Python -> WASM -> JS -> GPU has a cost. The computation must be "heavy" enough to justify this overhead.
*   **WASM Memory Access**: JS code needs to access Pyodide's memory to upload data to GPU buffers without unnecessary copies.
*   **API Verbosity**: The WebGPU API is verbose and requires a structured approach to state management (pipelines, bind groups).

## Solution
Access the `navigator.gpu` API via Pyodide's `js` module. Use NumPy for efficient memory layout on the Python side, and pass the underlying memory views to the WebGPU `writeBuffer` and `mapAsync` methods.

1.  **Request Device**: Use `await js.navigator.gpu.requestAdapter()` and `requestDevice()`.
2.  **Buffer Management**: Create GPU buffers with appropriate usage flags (`STORAGE`, `COPY_SRC`, `COPY_DST`).
3.  **Shader Integration**: Write kernels in WGSL (WebGPU Shading Language) as Python strings.
4.  **Zero-Copy (ish) Transfer**: Use `input_numpy_array.data` or `memoryview` to pass pointers to JS without full serialization.

## Implementation

### The WebGPU Pattern (Python)
```python
import js
import numpy as np

async def compute_on_gpu(data_list):
    # 1. Setup
    adapter = await js.navigator.gpu.requestAdapter()
    device = await adapter.requestDevice()
    
    # 2. Data Preparation
    input_data = np.array(data_list, dtype=np.float32)
    size = input_data.nbytes
    
    # 3. Create GPU Buffers
    input_buffer = device.createBuffer({
        "size": size,
        "usage": js.GPUBufferUsage.STORAGE | js.GPUBufferUsage.COPY_DST
    })
    
    # 4. Upload data
    # Passing the .data (memoryview) is the most efficient bridge
    device.queue.writeBuffer(input_buffer, 0, input_data.data)
    
    # ... setup pipeline and dispatch ...
```

## Resulting Context
*   **Pros**: Massive speedups for parallel workloads. Offloads work from the main thread's CPU.
*   **Cons**: Limited browser support (requires modern browsers). High implementation complexity compared to pure Python. Debugging shaders in the browser can be difficult.

## Related Patterns
*   **Proxy Memory Management**: Critical for cleaning up GPU-related JS objects and Python memory views.
*   **Worker RPC**: WebGPU is often combined with Web Workers to prevent UI jank during long compute passes.

## Verification
*   **Example**: `examples/loading/webgpu_compute.html`
*   **Note**: Automated testing of WebGPU in CI environments often requires specific hardware acceleration and browser flags.
