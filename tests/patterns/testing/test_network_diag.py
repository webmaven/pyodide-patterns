import pytest
import time
from playwright.sync_api import Page, expect

BASE_URL = "https://webmaven.github.io/pyodide-patterns/"

def test_diagnose_blocked_resources(page: Page):
    """
    Systematically checks for resources blocked by COEP/CORP.
    """
    url = f"{BASE_URL}examples/loading/python_ui_offloading.html"
    print(f"\nDIAGNOSING: {url}")

    failed_requests = []
    page.on("requestfailed", lambda req: failed_requests.append(f"{req.url}: {req.failure}"))
    
    logs = []
    page.on("console", lambda msg: logs.append(f"[{msg.type}] {msg.text}"))

    # 1. Navigate
    page.goto(url)
    
    # 2. Wait for stabilization
    time.sleep(10)

    # 3. Check State
    metrics = page.evaluate("""() => {
        return {
            isolated: window.crossOriginIsolated,
            sw_controlled: !!navigator.serviceWorker.controller,
            pyodide_defined: !!window.pyodide
        }
    }""")
    
    print(f"    Environment -> Isolated: {metrics['isolated']}, SW: {metrics['sw_controlled']}, Pyodide: {metrics['pyodide_defined']}")

    # 4. Analyze Failures
    print("\n--- Network Failures ---")
    for req in failed_requests:
        print(f"  ❌ {req}")
        
    print("\n--- Relevant Console Logs ---")
    for l in logs:
        if any(keyword in l.lower() for keyword in ["block", "coep", "corp", "cross-origin", "cors"]):
            print(f"  ⚠️ {l}")
