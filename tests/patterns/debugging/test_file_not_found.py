# File not found / 404 handling test

import pytest
from playwright.sync_api import Error, Page


@pytest.mark.xfail(reason="Demonstrating file not found error handling")
def test_handles_file_not_found_error(page: Page, live_server: str):
    """
    Navigate to a non‑existent file and assert the correct Playwright error
    is raised.
    """
    # Construct a URL to a file that does not exist in the served directory
    missing_path = f"{live_server}/non_existent.html"
    with pytest.raises(Error, match="net::ERR_FILE_NOT_FOUND"):
        page.goto(missing_path)
