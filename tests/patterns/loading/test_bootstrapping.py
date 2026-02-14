import pytest
from playwright.sync_api import Page, expect

def test_progressive_bootstrapping_milestones(page: Page, live_server: str):
    """
    Verify that the bootstrapping process hits specific milestones in order.
    """
    page.goto(f"{live_server}/examples/loading/progressive_bootstrapping.html")
    
    # 1. Check initial status
    expect(page.locator("#status")).to_contain_text("Downloading WASM")
    
    # 2. Wait for WASM milestone
    expect(page.locator("#m-wasm")).to_have_class("milestone complete", timeout=30000)
    
    # 3. Wait for Python milestone
    expect(page.locator("#m-python")).to_have_class("milestone complete", timeout=30000)
    
    # 4. Wait for Package milestone
    expect(page.locator("#m-packages")).to_have_class("milestone complete", timeout=30000)
    
    # 5. Verify App Reveal
    expect(page.locator("#app-content")).to_be_visible(timeout=10000)
    expect(page.locator("#output")).to_contain_text("NumPy version:")
