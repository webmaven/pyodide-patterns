# This file will contain tests for asynchronous race conditions.
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.xfail(strict=True, reason="This test is designed to fail to demonstrate a race condition.")
def test_async_race_condition_failure(page: Page, live_server: str):
    """
    This test demonstrates a common race condition failure.

    It clicks a button that triggers a slow (2-second) async operation,
    but it checks for the result *immediately* without waiting. This will
    cause the test to fail with a timeout.

    This test is marked as xfail because it is *supposed* to fail.
    """
    page.goto(f"{live_server}/examples/debugging/race_condition.html")

    # Wait for Pyodide to be ready before starting the test
    expect(page.locator("#result-container")).to_have_text(
        "Pyodide loaded. Ready to start.",
        timeout=60000
    )

    # Click the button to start the slow process
    page.locator("#start-button").click()

    # !! THIS IS THE MISTAKE !!
    # The test immediately checks for the success message without waiting for
    # the 2-second Python script to finish.
    success_message = page.locator("#success-message")

    # This assertion will time out and fail, because the element doesn't exist yet.
    # We use a short timeout to make the failure faster.
    expect(success_message).to_be_visible(timeout=500)


def test_async_race_condition_success(page: Page, live_server: str):
    """
    This test demonstrates the CORRECT way to handle an async operation.

    It clicks the button that triggers the slow operation, and then uses a
    single `expect` call with a sufficient timeout to wait for the result.
    Playwright's web-first assertions will automatically retry the check
    until the element appears or the timeout is reached.
    """
    page.goto(f"{live_server}/examples/debugging/race_condition.html")

    # Wait for Pyodide to be ready
    expect(page.locator("#result-container")).to_have_text(
        "Pyodide loaded. Ready to start.",
        timeout=60000
    )

    # Click the button to start the slow process
    page.locator("#start-button").click()

    # !! THIS IS THE CORRECT WAY !!
    # We create a locator for the element we expect to appear, and then
    # use `expect` with a timeout that is longer than the slow operation.
    success_message = page.locator("#success-message")

    # This assertion will now pass, because Playwright will wait up to 5 seconds
    # for the element to become visible.
    expect(success_message).to_be_visible(timeout=5000)
    expect(success_message).to_have_text("Slow process complete!")
