import pytest
from playwright.sync_api import Page, expect


@pytest.mark.xfail(
    reason=(
        "Isolated environments often block CDN resources that lack CORP headers, "
        "preventing Pyodide from loading."
    )
)
def test_shared_memory_gpu_execution(page: Page, isolated_server: str):
    """
    Verify that Python can manipulate a JS-created SharedArrayBuffer
    and the changes are visible back in JS.
    """
    page.on("console", lambda msg: print(f"Browser Console: {msg.text}"))
    page.goto(f"{isolated_server}/examples/loading/shared_memory_gpu.html")

    # 1. Verify Isolation
    expect(page.locator("#isolation-status")).to_have_text(
        "Environment is cross-origin isolated. SAB available.", timeout=30000
    )

    # 2. Run Compute
    run_btn = page.locator("#run-btn")
    expect(run_btn).to_be_enabled(timeout=60000)
    run_btn.click()

    # 3. Verify Result
    # Initial was 10,20,30,40. Python multiplies by 2. Result should be 20,40,60,80
    expect(page.locator("#output")).to_contain_text("20,40,60,80")
    expect(page.locator("#output")).to_contain_text(
        "Verification: JS view matches Python result."
    )
