# Incorrect text assertion test


import pytest
from playwright.sync_api import Page, expect


@pytest.mark.xfail(reason="Demonstrating incorrect text assertion failure")
def test_incorrect_text_assertion(page: Page, live_server: str):
    """
    Navigate to the index page and deliberately assert the wrong title to
    demonstrate a failure.
    """
    page.goto(f"{live_server}/examples/index.html")
    # This will fail because the actual title is "Playwright Console Debugging"
    expect(page.locator("h1")).to_have_text("Goodbye")
