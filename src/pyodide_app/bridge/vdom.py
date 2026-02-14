import js
from typing import Any, Dict, List, Optional, Union
from pyodide.ffi import create_proxy
from .core import keep_alive

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
