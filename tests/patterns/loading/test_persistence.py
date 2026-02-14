from playwright.sync_api import Page, expect


def test_idbfs_persistence(page: Page, live_server: str):
    """
    Verify that data written to IDBFS survives a page reload.
    """
    url = f"{live_server}/examples/loading/persistence.html"
    page.goto(url)

    # 1. Wait for initialization
    expect(page.locator("#status")).to_have_text(
        "Pyodide Ready. File system mounted.", timeout=30000
    )

    # 2. Write data
    test_string = "Persisted Data 123"
    page.locator("#file-content").fill(test_string)
    page.locator("#save-btn").click()

    # Wait for the save operation to complete (syncfs is async)
    expect(page.locator("#status")).to_have_text("Saved successfully!", timeout=10000)

    # 3. Reload the page
    page.reload()

    # 4. Wait for re-initialization (and automatic syncfs(true))
    expect(page.locator("#status")).to_have_text(
        "Pyodide Ready. File system mounted.", timeout=30000
    )

    # 5. Read the data back
    page.locator("#load-btn").click()
    expect(page.locator("#output")).to_have_text(test_string)
