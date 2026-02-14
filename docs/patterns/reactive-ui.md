# Reactive UI Patterns

## Context
Standard DOM manipulation in Pyodide involves manual imperative calls (`js.document.getElementById(...)`). As applications grow in complexity, managing the synchronization between Python state and the browser UI becomes error-prone. Reactive patterns automate this synchronization by binding Python state directly to DOM representation.

## Problem
How can we ensure the UI stays in sync with Python data structures without writing repetitive boilerplate code for every state change, while balancing performance and code complexity?

## Forces
*   **Performance**: Bridging WASM (Python) to the JS DOM is expensive. Frequent or massive updates can cause UI lag.
*   **Boilerplate**: Manual DOM manipulation is verbose and hard to maintain as the UI scales.
*   **Pythonicity**: Developers want to use idiomatic Python (classes, decorators, properties) rather than jumping between languages.
*   **Memory Management**: Reactive event listeners and observers create JS-Python proxies that must be managed to avoid memory leaks.

## Solution Implementations

### 1. Observer-based (Dataclasses)
Uses a custom `@observable` decorator on a standard Python `@dataclass`.
*   **Mechanism**: Intercepts `__setattr__` to trigger callbacks.
*   **Ideal Use Case**: Simple forms, settings panels, and dashboards where specific pieces of state map to specific DOM elements.
*   **Trade-offs**:
    *   **Pros**: Zero external dependencies; extremely low overhead; very clean "Plain Old Python Object" (POPO) feel.
    *   **Cons**: Requires manual "wiring" (binding) of each state field to a DOM ID. Not suitable for dynamic lists where elements are added or removed frequently.
*   **Resulting Context**: Application state is fully decoupled from the UI. Developers can focus on Python data logic, only thinking about the DOM during initial setup. However, reliance on manual DOM IDs can become brittle in large-scale applications.
*   **Verification**: `examples/loading/reactive_observer.html`

### 2. Virtual DOM (Pure Python)
A declarative approach where Python defines the UI as a tree of nested dictionaries.
*   **Mechanism**: A Python reconciler compares the new virtual tree with the previous one and patches the real DOM.
*   **Ideal Use Case**: Complex applications with dynamic structures, nested components, and lists that change size or order.
*   **Trade-offs**:
    *   **Pros**: Full declarative control; handles complex UI logic easily; 100% Python engine.
    *   **Cons**: "Heavy" compared to observers; every update requires generating a new tree structure; can hit WASM-JS bridge limits on extremely large trees.
*   **Resulting Context**: The implementation provided in this cookbook is a **Naive VDOM**. It uses a "Replacement" strategy where `replaceChildren()` is called on every update. While simple and robust for learning, a production-grade engine would implement a **Tree-Walking Diffing Algorithm** to modify only the specific DOM nodes that changed, significantly reducing the number of WASM-to-JS calls.
*   **Verification**: `examples/loading/reactive_vdom.html`

### 3. Signals (Fine-grained)
Uses functional "Signal" objects that maintain their own list of subscribers.
*   **Mechanism**: Each UI element subscribes directly to the data it needs.
*   **Ideal Use Case**: Real-time data visualizations, high-frequency updates, and apps where many independent elements change simultaneously.
*   **Trade-offs**:
    *   **Pros**: Most efficient execution; only the specific "leaf" nodes of the DOM update; no tree-walking or manual binding to IDs required.
    *   **Cons**: Requires using `.value` to access data; most sensitive to Python Garbage Collection (proxies must be held in scope).
*   **Resulting Context**: Achieves the theoretical maximum performance for Pyodide UI updates by minimizing WASM-JS bridge traversal. However, it requires significant developer discipline regarding proxy lifecycle management, making it the "Power User" choice for high-frequency data applications.
*   **Verification**: `examples/loading/reactive_signals.html`

## Comparison Matrix

| Feature | Observer | VDOM (Python) | Signals |
| :--- | :--- | :--- | :--- |
| **Logic Style** | Imperative Bindings | Declarative Tree | Functional Subscriptions |
| **Scale Range** | Small / Static | Medium / Dynamic | Large / High-Freq |
| **JS Bridge Hits** | Very Low | High (Tree generation) | Moderate |
| **Ergonomics** | 5/5 (Dataclasses) | 4/5 (Declarative) | 3/5 (Explicit Signals) |
| **Zero-JS** | Yes | Yes | Yes |

## Verification
*   **Test**: `tests/patterns/architectural/test_reactivity.py`
*   **Examples**: 
    *   `examples/loading/reactive_observer.html`
    *   `examples/loading/reactive_vdom.html`
    *   `examples/loading/reactive_signals.html`

## Implementation Example: Observer-based (Dataclasses)
By leveraging the modular bridge, we can keep state definitions entirely Pythonic.

```python
from pyodide_app.bridge.reactivity import observable
from dataclasses import dataclass

@observable
@dataclass
class AppState:
    count: int = 0

state = AppState()
state.subscribe("count", lambda v: print(f"Count is now {v}"))
state.count += 1 # Triggers the print and any bound UI elements
```

## Related Patterns
*   **Synchronous-Looking Async UI**: Reactive patterns are the best way to display data arriving asynchronously from background workers.
*   **Proxy Memory Management**: When using reactive components, always ensure that your event proxies are stored in a persistent Python variable to prevent premature cleanup by the garbage collector.
