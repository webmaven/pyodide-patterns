# External script loading failure tests

import os
import pytest
from playwright.sync_api import Page, expect, Error

def test_external_script_success(page: Page, live_server: str):
    """Load a page that includes a valid external script and verify it runs without error."""
    page.goto(f"{live_server}/examples/debugging/external_script.html")
    # The script adds a p tag with id 'loaded-message'
    expect(page.locator("#loaded-message")).to_be_visible()

@pytest.mark.xfail(reason="Demonstrating network failure capture")
def test_external_script_404_failure(page: Page, live_server: str):
    """Navigate to a page that references a missing external script and assert a requestfailed event."""
    messages = []
    page.on("requestfailed", lambda r: messages.append(r))
    page.goto(f"{live_server}/examples/debugging/script_not_found.html")
    # Expect at least one failed request for the missing script
    assert any("script_not_found.js" in r.url for r in messages), "Missing script request not captured"

@pytest.mark.xfail(reason="Demonstrating runtime error capture")
def test_external_script_runtime_error(page: Page, live_server: str):
    """Load a page with an external script that throws an error and capture the pageerror event."""
    errors = []
    page.on("pageerror", lambda e: errors.append(e))
    page.goto(f"{live_server}/examples/debugging/script_runtime_error.html")
    # The script should cause a runtime error; verify we captured it
    assert errors, "Expected a runtime error from the external script"
    # Optionally check the error message contains a known substring
    assert any("ReferenceError" in str(err) for err in errors), "Unexpected error type"
