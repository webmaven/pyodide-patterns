import asyncio

import pytest


@pytest.mark.asyncio
@pytest.mark.xfail(
    reason="Event loop conflict between pytest-asyncio and pytest-playwright"
)
async def test_async_conflict_demo():
    """
    This test demonstrates the conflict between pytest-asyncio and pytest-playwright.
    When run in the same test suite, pytest-asyncio's attempt to manage the event loop
    often conflicts with Playwright's own event loop management, leading to a
    RuntimeError.

    The recommended solution is to isolate integration tests that require
    pytest-asyncio into a separate test directory with its own configuration.
    """
    await asyncio.sleep(0.1)
    assert True
