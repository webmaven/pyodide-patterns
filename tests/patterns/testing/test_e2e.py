from playwright.sync_api import Page, expect


def test_greeting_e2e_playwright(page: Page, http_server):
    """
    An end-to-end test using Playwright that covers a complete user scenario.
    """
    logs = []
    page.on("console", lambda msg: logs.append(msg.text))

    page.goto(f"{http_server}/index.html")

    # Find the elements
    title = page.locator("#title")
    name_input = page.locator("#name")
    greet_button = page.locator("#greet-button")

    # 1. Initial state
    try:
        expect(title).to_have_text("Hello, World!", timeout=30000)
    finally:
        print("\nBrowser Console Logs:")
        for log in logs:
            print(log)

    # 2. Enter name and greet
    name_input.fill("Jules")
    greet_button.click()
    expect(title).to_have_text("Hello, Jules!")

    # 3. Clear input and greet again
    name_input.fill("")
    greet_button.click()
    expect(title).to_have_text("Hello, World!")

    # 4. Take a screenshot
    page.screenshot(
        path="pyodide-patterns/tests/screenshots/e2e_playwright_screenshot.png"
    )
