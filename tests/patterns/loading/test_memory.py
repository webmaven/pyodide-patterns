from playwright.sync_api import Page, expect


def test_proxy_destruction_validity(page: Page, live_server: str):
    """
    Verify that calling .destroy() makes the proxy unusable.
    """
    page.goto(f"{live_server}/examples/loading/proxy_management.html")

    # Wait for Pyodide
    expect(page.locator("#status")).to_have_text("Pyodide Ready.", timeout=30000)

    # Run a script to create and destroy a proxy, then try to use it
    # We expect an error if we try to use a destroyed proxy.
    is_destroyed = page.evaluate("""
        async () => {
            const proxy = pyodide.runPython("[1, 2, 3]");
            proxy.destroy();
            try {
                proxy.toJs();
                return false; // Should have failed
            } catch (e) {
                return e.message.includes("destroyed");
            }
        }
    """)

    assert is_destroyed is True


def test_cleanup_button_interaction(page: Page, live_server: str):
    """
    Verify the example page buttons work.
    """
    page.goto(f"{live_server}/examples/loading/proxy_management.html")
    expect(page.locator("#status")).to_have_text("Pyodide Ready.", timeout=30000)

    cleanup_btn = page.locator("#cleanup-btn")
    cleanup_btn.click()

    expect(page.locator("#output")).to_contain_text(
        "Created and destroyed 1000 proxies"
    )
