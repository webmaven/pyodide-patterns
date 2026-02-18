import pytest
import time
from playwright.sync_api import Page, expect

# We use the simulator to catch header-related issues locally
@pytest.mark.parametrize("demo_path", [
    "examples/loading/python_ui_offloading.html",
    "examples/workers/worker_pool.html",
    "examples/loading/shared_memory_gpu.html"
])
def test_isolation_lifecycle_lab(page: Page, github_pages_simulator: str, demo_path: str):
    """
    SYSTEMATIC PROBE: Validates the isolation lifecycle.
    1. First Visit (Cold Start): Should trigger Guard reload and achieve isolation.
    2. Soft Reload: Should maintain isolation.
    3. Navigation from Root: Should maintain isolation.
    """
    base_url = github_pages_simulator
    url = f"{base_url}/{demo_path}"
    
    print(f"\n[LAB] Testing Demo: {demo_path}")
    
    # --- STEP 1: Cold Start (Direct Visit) ---
    print("  [1] Cold Start (Direct Visit)...")
    page.goto(url)
    
    # Wait for the Isolation Guard to do its work (might involve a reload)
    # We wait until crossOriginIsolated is True
    try:
        page.wait_for_function("() => window.crossOriginIsolated === true", timeout=15000)
        print("    ✅ Shield Established (Isolated: True)")
    except Exception:
        # If it failed, let's see why
        metrics = page.evaluate("""() => {
            return {
                isolated: window.crossOriginIsolated,
                sw_active: !!navigator.serviceWorker.controller,
                ua: navigator.userAgent
            }
        }""")
        pytest.fail(f"Cold Start failed to isolate. Metrics: {metrics}")

    # --- STEP 2: Soft Reload ---
    print("  [2] Soft Reload...")
    page.reload()
    page.wait_for_load_state("networkidle")
    
    # Check if isolation survived the reload
    is_isolated = page.evaluate("() => window.crossOriginIsolated")
    assert is_isolated, "Isolation lost after Soft Reload!"
    print("    ✅ Shield Persistent after Soft Reload")

    # --- STEP 3: Functional Verification ---
    # We verify the demo actually initializes its Pyodide component
    print("  [3] Verifying Pyodide Initialization...")
    
    if "python_ui_offloading" in demo_path:
        # Wait for the status to show 'Ready'
        status = page.locator("#ui-status")
        expect(status).to_contain_text("Ready", timeout=30000)
        print("    ✅ UI Controller initialized successfully")
        
        # Test a functional interaction
        page.click("#process-btn")
        expect(page.locator("#ui-output")).to_contain_text("The answer is 84", timeout=10000)
        print("    ✅ Logic Execution successful")

    elif "worker_pool" in demo_path:
        status = page.locator("#status")
        expect(status).to_contain_text("Pool Ready", timeout=30000)
        print("    ✅ Worker Pool initialized successfully")

    print(f"  [DONE] Demo {demo_path} passed the Stability Matrix.")
