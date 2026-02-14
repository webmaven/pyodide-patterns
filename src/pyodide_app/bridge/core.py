import sys
from typing import Any, List

# Environment detection
IS_EMSCRIPTEN = sys.platform == "emscripten"

# --- GC Management ---

_GLOBAL_PROXIES: List[Any] = []

def keep_alive(proxy: Any) -> Any:
    """
    Prevents a PyProxy from being garbage collected by storing it in a global list.
    Use this for event listeners or components that must persist.
    """
    _GLOBAL_PROXIES.append(proxy)
    return proxy
