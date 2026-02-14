import js
import os
from typing import List, Dict, Any
from pyodide_app.bridge.core import keep_alive
from pyodide.ffi import create_proxy

class FSExplorer:
    def __init__(self, root_id: str):
        self.root_el = js.document.getElementById(root_id)
        self.refresh()

    def get_tree(self, path: str = "/home") -> Dict[str, Any]:
        """Walk the VFS and return a nested dictionary."""
        name: str = os.path.basename(path) or path
        node: Dict[str, Any] = {"name": name, "path": path, "type": "dir", "children": []}
        
        try:
            # Skip massive system directories for this pattern's safety
            if path in ["/lib", "/dev", "/proc"]:
                return node

            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    # Limit depth to 2 for the cookbook demonstration
                    if path.count("/") < 3:
                        node["children"].append(self.get_tree(full_path))
                else:
                    node["children"].append({
                        "name": item, 
                        "path": full_path, 
                        "type": "file",
                        "size": os.path.getsize(full_path)
                    })
        except Exception as e:
            node["name"] = str(node["name"]) + f" (Error: {e})"
            
        return node

    def render_node(self, node: Dict[str, Any]) -> Any:
        li = js.document.createElement("li")
        li.className = f"fs-node {node['type']}"
        
        span = js.document.createElement("span")
        icon = "📁" if node["type"] == "dir" else "📄"
        size_info = f" ({node.get('size', 0)} bytes)" if node["type"] == "file" else ""
        span.innerText = f"{icon} {node['name']}{size_info}"
        li.appendChild(span)

        if node["type"] == "dir" and node["children"]:
            ul = js.document.createElement("ul")
            for child in node["children"]:
                ul.appendChild(self.render_node(child))
            li.appendChild(ul)
        
        return li

    def refresh(self) -> None:
        self.root_el.innerHTML = ""
        # Start walk at /home for performance and reliability
        tree = self.get_tree("/home")
        self.root_el.appendChild(self.render_node(tree))

def init_explorer() -> None:
    # Create some dummy files in /home/pyodide
    base = "/home/pyodide"
    if not os.path.exists(base):
        os.makedirs(base)
        
    with open(f"{base}/hello.py", "w") as f:
        f.write("print('Hello from VFS')")
        
    os.makedirs(f"{base}/data", exist_ok=True)
    with open(f"{base}/data/config.json", "w") as f:
        f.write("{}")
        
    explorer = FSExplorer("fs-root")
    js.explorer_instance = create_proxy(explorer)

init_explorer()
