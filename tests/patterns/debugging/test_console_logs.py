# Console log capture on failure

import os
import pytest
from playwright.sync_api import Page, expect, Error

@pytest.mark.xfail(reason="Demonstrating console log capture on failure")
def test_captures_console_logs_on_failure(page: Page, live_server: str):
    """Capture console logs when a test fails, mirroring the original pattern."""
    messages = []
    page.on("console", lambda msg: messages.append(msg.text))

    # Navigate to a page that will intentionally fail the assertion
    page.goto(f"{live_server}/examples/index.html")

    try:
        # Expect an element that does not exist to trigger failure
        expect(page.locator("#nonexistent")).to_be_visible(timeout=1000)
    except Exception as e:
        print("\n--- Captured Console Logs ---")
        for msg in messages:
            print(msg)
        print("---------------------------\n")
        raise e
