from playwright.sync_api import Page, expect


def test_greet_button_playwright(page: Page, http_server):
    """
    A functional test using Playwright to verify that the greet button
    updates the heading with a personalized greeting.
    """
    page.goto(f"{http_server}/index.html")

    # Find the elements
    title = page.locator("#title")
    name_input = page.locator("#name")
    greet_button = page.locator("#greet-button")

    # It might take a moment for Pyodide to load and run the initial script.
    # We should wait for the initial text to be set.
    expect(title).to_have_text("Hello, World!", timeout=30000) # Increased timeout

    # Interact with the page
    name_input.fill("Jules")
    greet_button.click()

    # Assert the result
    expect(title).to_have_text("Hello, Jules!")
