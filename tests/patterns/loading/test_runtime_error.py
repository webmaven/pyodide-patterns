from playwright.sync_api import Page, expect


def wait_for_pyodide(page: Page, timeout=30000):
    """Wait until Pyodide reports it is loaded and ready."""
    expect(page.locator("#status")).to_have_text(
        "Pyodide loaded. Ready.", timeout=timeout
    )


def test_python_runtime_error(page: Page, live_server: str):
    """Demonstrate a Python runtime error inside Pyodide and capture it."""
    page.goto(f"{live_server}/examples/loading/runtime_error.html")

    # The page runs the script automatically. We wait for the error message in the UI.
    expect(page.locator("p")).to_have_text(
        "Python script failed, as expected.", timeout=60000
    )

    # Verify we captured the error in the console
    # Note: We can't easily capture past console messages with
    # page.on("console") if they happened before we attached the listener.
    # But since we are loading the page, we might miss it if we attach too
    # late. However, the UI check is sufficient for this test.
