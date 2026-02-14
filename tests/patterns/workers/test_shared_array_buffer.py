from playwright.sync_api import Page, expect


def test_shared_array_buffer_unavailability(page: Page, live_server: str):
    """
    Verify that SharedArrayBuffer is NOT available on a standard live_server
    without COOP/COEP headers.
    """
    page.goto(f"{live_server}/examples/workers/shared_array_buffer.html")

    status = page.locator("#status")
    coop_coep = page.locator("#coop-coep")

    expect(coop_coep).to_have_text("Environment is NOT cross-origin isolated.")
    expect(status).to_have_text("SharedArrayBuffer is NOT defined.")


def test_shared_array_buffer_availability(page: Page, isolated_server: str):
    """
    Verify that SharedArrayBuffer IS available when COOP/COEP headers are present.
    """
    page.goto(f"{isolated_server}/examples/workers/shared_array_buffer.html")

    status = page.locator("#status")
    coop_coep = page.locator("#coop-coep")

    expect(coop_coep).to_have_text(
        "Environment is cross-origin isolated (COOP/COEP active)."
    )
    expect(status).to_have_text("SharedArrayBuffer is AVAILABLE.")
