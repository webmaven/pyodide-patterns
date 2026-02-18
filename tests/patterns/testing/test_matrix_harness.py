import pytest
import time
from playwright.sync_api import Page, expect

@pytest.mark.parametrize("demo_path", [
    "examples/loading/python_ui_offloading.html",
    "examples/workers/worker_pool.html",
    "examples/loading/shared_memory_gpu.html"
])
def test_isolation_lifecycle_lab(page: Page, github_pages_simulator: str, demo_path: str):
    base_url = github_pages_simulator
    url = f"{base_url}/{demo_path}"
    
    # --- ERROR GUARD ---
    fatal_errors = []
    page.on("console", lambda msg: fatal_errors.append(msg.text) if msg.type == "error" else None)
    page.on("pageerror", lambda exc: fatal_errors.append(str(exc)))

    print(f"\n[LAB] Testing Demo: {demo_path}")
    
    # --- STEP 1: Cold Start ---
    print("  [1] Cold Start (Direct Visit)...")
    page.goto(url)
    
    # Wait for the Isolation Guard
    page.wait_for_function("() => window.crossOriginIsolated === true", timeout=15000)
    
    # --- STEP 2: Error Check ---
    # We fail immediately if any fatal script errors occurred
    for err in fatal_errors:
        if any(keyword in err for keyword in ["SyntaxError", "ReferenceError", "TypeError"]):
            pytest.fail(f"Fatal script error detected during load: {err}")

    # --- STEP 3: Functional Verification ---
    print("  [3] Verifying Pyodide Initialization...")
    
    if "python_ui_offloading" in demo_path:
        status = page.locator("#ui-status")
        expect(status).to_contain_text("Ready", timeout=30000)
        print("    ✅ UI Controller initialized successfully")
        
        page.click("#process-btn")
        expect(page.locator("#ui-output")).to_contain_text("The answer is 84", timeout=15000)
        print("    ✅ Logic Execution successful")

    print(f"  [DONE] Demo {demo_path} passed the Stability Matrix.")
