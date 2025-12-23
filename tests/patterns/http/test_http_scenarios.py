# HTTP server scenario tests

from playwright.sync_api import Page, expect


def test_http_page_has_correct_title(page: Page, live_server: str):
    """Navigate to the index page served over HTTP and verify the title."""
    page.goto(f"{live_server}/examples/index.html")
    expect(page).to_have_title("Playwright Console Debugging")

def test_http_file_not_found(page: Page, live_server: str):
    """Request a non‑existent file over HTTP and assert the correct response status."""
    missing_url = f"{live_server}/non_existent.html"
    response = page.goto(missing_url)
    assert response.status == 404
