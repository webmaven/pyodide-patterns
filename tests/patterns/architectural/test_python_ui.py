from playwright.sync_api import Page, expect


def test_python_ui_offloading_responsiveness(page: Page, live_server: str):
    """
    Verify that the UI remains responsive and updates via the Python controller.
    """
    page.goto(f"{live_server}/examples/loading/python_ui_offloading.html")

    # 1. Wait for Python UI to be ready
    expect(page.locator("#ui-status")).to_have_text(
        "Python UI Controller Ready.", timeout=60000
    )

    btn = page.locator("#process-btn")
    expect(btn).to_be_enabled()

    # 2. Trigger the heavy computation
    btn.click()

    # 3. Verify immediate UI feedback from Python main thread
    expect(page.locator("#ui-status")).to_contain_text("Worker calculating")
    expect(page.locator("#ui-spinner")).to_be_visible()
    expect(btn).to_be_disabled()

    # 4. Wait for the background result (3s sleep + bootstrap)
    expect(page.locator("#ui-output")).to_have_text("The answer is 84", timeout=15000)
    expect(page.locator("#ui-spinner")).to_be_hidden()
    expect(page.locator("#ui-status")).to_have_text("Computation complete.")
    expect(btn).to_be_enabled()
