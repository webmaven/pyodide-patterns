import pytest
import time
from playwright.sync_api import Page, expect

# The target for our systematic investigation
BASE_URL = "https://webmaven.github.io/pyodide-patterns/"

def test_behavioral_offloading(page: Page):
    full_url = f"{BASE_URL}examples/loading/python_ui_offloading.html"
    print(f"\nSTART BEHAVIORAL TEST: {full_url}")

    logs = []
    page.on("console", lambda msg: logs.append(f"[{msg.type}] {msg.text}"))
    page.on("pageerror", lambda exc: logs.append(f"[ERROR] {exc}"))

    page.goto(full_url)
    
    # 1. Wait for Ready
    status = page.locator("#ui-status")
    expect(status).to_have_text("Python UI Controller Ready.", timeout=30000)
    print("    Page is Ready.")

    # 2. Click Button
    btn = page.locator("#process-btn")
    btn.click()
    print("    Button Clicked.")

    # 3. Wait for result (expected after 3s sleep in worker)
    output = page.locator("#ui-output")
    try:
        expect(output).to_have_text("The answer is 84", timeout=15000)
        print("    SUCCESS: Result received.")
    except Exception as e:
        print(f"    FAILURE: Result not received. Timeout reached.")
        print("    CONSOLE LOGS:")
        for l in logs: print(f"      {l}")
        raise e
