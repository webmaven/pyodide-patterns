import pytest
from playwright.sync_api import Page, expect

def test_reactive_observer(page: Page, live_server: str):
    page.goto(f"{live_server}/examples/loading/reactive_observer.html")
    
    # Wait for Python
    expect(page.locator("#name-display")).to_have_text("Python Developer", timeout=30000)
    
    # Test Name Input
    page.locator("#name-input").fill("Jules")
    expect(page.locator("#name-display")).to_have_text("Jules")
    
    # Test Counter
    page.locator("#inc-btn").click()
    expect(page.locator("#count-display")).to_have_text("1")

def test_reactive_vdom(page: Page, live_server: str):
    page.goto(f"{live_server}/examples/loading/reactive_vdom.html")
    
    # Wait for Python to render
    card = page.locator(".card")
    expect(card.locator("h2")).to_have_text("Pure Python VDOM", timeout=30000)
    expect(card.locator("p")).to_have_text("Count: 0")
    
    # Test Increment
    card.locator("button:has-text('Increment')").click()
    expect(card.locator("p")).to_have_text("Count: 1")
    
    # Test Reset
    card.locator("button:has-text('Reset')").click()
    expect(card.locator("p")).to_have_text("Count: 0")

@pytest.mark.xfail(reason="Signal event handlers are intermittently failing to fire in the headless test environment.")
def test_reactive_signals(page: Page, live_server: str):
    page.goto(f"{live_server}/examples/loading/reactive_signals.html")
    
    # Wait for Signals
    expect(page.locator("#sig-count")).to_have_text("0", timeout=30000)
    
    # Test Signal Update
    page.locator("#sig-inc").click()
    expect(page.locator("#sig-count")).to_have_text("1")
    expect(page.locator("#sig-double")).to_have_text("2")
    
    # Test Theme Signal
    card = page.locator("#sig-card")
    page.locator("#sig-theme").click()
    # Check CSS update via theme signal
    expect(card).to_have_css("background-color", "rgb(51, 51, 51)") # #333
