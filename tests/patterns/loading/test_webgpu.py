import pytest
from playwright.sync_api import Page, expect


def test_webgpu_support_reporting(page: Page, live_server: str):
    """
    Verify that the page correctly reports WebGPU support.
    """
    page.goto(f"{live_server}/examples/loading/webgpu_compute.html")

    # Wait for status
    expect(page.locator("#gpu-support")).to_be_visible()

    status_text = page.locator("#gpu-support").inner_text()
    print(f"WebGPU Support Status: {status_text}")


@pytest.mark.skip(
    reason=(
        "WebGPU is often unavailable in headless CI environments without "
        "specific hardware and flags."
    )
)
def test_webgpu_compute_execution(page: Page, live_server: str):
    """
    Attempt to run a WebGPU compute shader and verify the result.
    This test is skipped by default as it requires a GPU-enabled browser.
    """
    page.goto(f"{live_server}/examples/loading/webgpu_compute.html")

    # Wait for Pyodide
    expect(page.locator("#status")).to_have_text("Pyodide Ready.", timeout=60000)

    compute_btn = page.locator("#compute-btn")
    if compute_btn.is_enabled():
        compute_btn.click()
        expect(page.locator("#output")).to_contain_text(
            "Result: [2,4,6,8]", timeout=30000
        )
    else:
        pytest.skip("WebGPU not supported in this browser instance.")
