from playwright.sync_api import Page, expect


def test_comlink_rpc_execution(page: Page, live_server: str):
    """
    Verify that Python code can be executed via a Comlink-wrapped worker.
    """
    page.goto(f"{live_server}/examples/workers/comlink_rpc.html")

    status = page.locator("#status")
    run_btn = page.locator("#run-btn")
    output = page.locator("#output")

    # Wait for initialization
    expect(status).to_have_text("Pyodide Ready.", timeout=60000)
    expect(run_btn).to_be_enabled()

    # Run Python code via RPC
    run_btn.click()
    expect(output).to_have_text("Result: 4")
