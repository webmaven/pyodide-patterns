import js
from typing import Any, Callable, Dict, List, Optional, Union
from pyodide.ffi import create_proxy

# --- GC Management ---

_GLOBAL_PROXIES: List[Any] = []

def keep_alive(proxy: Any) -> Any:
    """
    Prevents a PyProxy from being garbage collected by storing it in a global list.
    Use this for event listeners or components that must persist.
    """
    _GLOBAL_PROXIES.append(proxy)
    return proxy

# --- Reactive Signals ---

class Signal:
    """A fine-grained reactive signal."""
    def __init__(self, value: Any):
        self._value = value
        self._subscribers: List[Callable] = []

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, new_value: Any):
        self._value = new_value
        self._notify()

    def subscribe(self, callback: Callable):
        self._subscribers.append(callback)
        callback(self._value)

    def _notify(self):
        for cb in self._subscribers:
            cb(self._value)

# --- Observable Dataclasses ---

def observable(cls: Any) -> Any:
    """Decorator that adds subscription capabilities to a class."""
    orig_init = cls.__init__
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        object.__setattr__(self, '_subscribers', {})
        orig_init(self, *args, **kwargs)
        
    def subscribe(self, field_name: str, callback: Callable[[Any], None]) -> None:
        if field_name not in self._subscribers:
            self._subscribers[field_name] = []
        self._subscribers[field_name].append(callback)
        callback(getattr(self, field_name))

    def __setattr__(self, name: str, value: Any) -> None:
        object.__setattr__(self, name, value)
        if hasattr(self, '_subscribers') and name in self._subscribers:
            for cb in self._subscribers[name]:
                cb(value)

    cls.__init__ = __init__
    cls.subscribe = subscribe
    cls.__setattr__ = __setattr__
    return cls

# --- Virtual DOM Engine ---

def h(tag: str, props: Optional[Dict[str, Any]] = None, children: Any = None) -> Dict[str, Any]:
    """Hyperscript helper for Virtual Nodes."""
    return {
        "tag": tag, 
        "props": props or {}, 
        "children": children if isinstance(children, list) else ([children] if children else [])
    }

class PythonVDOM:
    """A minimal Pure Python Virtual DOM engine."""
    def __init__(self, container_id: str) -> None:
        self.container = js.document.getElementById(container_id)

    def _create_element(self, vnode: Union[Dict[str, Any], str]) -> Any:
        if isinstance(vnode, str):
            return js.document.createTextNode(vnode)
        
        el = js.document.createElement(vnode["tag"])
        
        for name, value in vnode["props"].items():
            if name.startswith("on"):
                # Automatically wrap event handlers in proxies if they aren't already
                # and keep them alive.
                callback = value
                if not hasattr(value, "destroy"):
                    callback = keep_alive(create_proxy(value))
                el.addEventListener(name[2:], callback)
            else:
                el.setAttribute(name, str(value))
        
        for child in vnode["children"]:
            el.appendChild(self._create_element(child))
        return el

    def patch(self, new_vtree: Dict[str, Any]) -> None:
        """Re-render the tree into the container."""
        new_dom = self._create_element(new_vtree)
        self.container.replaceChildren(new_dom)

# --- UI Helpers ---

def bind_to_dom(state_obj: Any, field: str, element_id: str, attr: str = "innerText") -> None:
    """Helper to bind an observable field directly to a DOM element."""
    def update_ui(val: Any) -> None:
        el = js.document.getElementById(element_id)
        if el:
            if attr == "value": el.value = str(val)
            else: setattr(el, attr, str(val))
    state_obj.subscribe(field, update_ui)
