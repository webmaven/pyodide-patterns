# Basic page sanity test

from playwright.sync_api import Page, expect


def test_page_has_correct_title(page: Page, live_server):
    """Navigate to the index page and verify the title is correct."""
    page.goto(f"{live_server}/examples/index.html")
    expect(page).to_have_title("Playwright Console Debugging")
