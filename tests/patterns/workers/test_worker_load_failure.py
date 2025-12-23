import pytest
from playwright.sync_api import Page, expect


def wait_for_pyodide(page: Page, timeout=30000):
    """Wait until Pyodide reports it is loaded and ready."""
    expect(page.locator("#status")).to_have_text("Pyodide loaded. Ready.", timeout=timeout)

@pytest.mark.xfail(reason="Demonstrating worker script load failure difficulty")
def test_worker_script_load_failure(page: Page, live_server: str, cross_origin_server: str):
    """Document the difficulty of reliably capturing a worker script load failure.
    This mirrors the commented‑out test in `pyodide-patterns/tests/patterns/workers/test_basic.py`.
    """
    page.goto(f"{live_server}/examples/workers/load_error.html")
    wait_for_pyodide(page)
    # Attempt to load a worker script from a server that does not send CORS headers.
    wheel_url = f"{cross_origin_server}/nonexistent_worker.js"
    with page.expect_console_message(lambda msg: "Access-Control-Allow-Origin" in msg.text) as console_info:
        page.evaluate(f"async () => await loadWorker('{wheel_url}')")
    expect(page.locator("#status")).to_contain_text("Failed to load worker")
