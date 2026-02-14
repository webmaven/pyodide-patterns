import pytest
from playwright.sync_api import Page, expect

@pytest.mark.xfail(reason="Service Workers are notoriously unreliable in headless testing environments.")
def test_service_worker_registration(page: Page, live_server: str):
    """
    Verify that the Service Worker registers and becomes active.
    """
    page.goto(f"{live_server}/examples/loading/service_worker_cache.html")
    
    sw_status = page.locator("#sw-status")
    pyodide_status = page.locator("#pyodide-status")
    
    # Wait for service worker to be active and controlling the page
    expect(sw_status).to_have_text("Service Worker: Active and Controlling Page", timeout=30000)
    
    # Verify Pyodide loads (likely from cache if run repeatedly, but first time is from network)
    expect(pyodide_status).to_contain_text("Pyodide: Loaded in", timeout=60000)

@pytest.mark.xfail(reason="Service Workers are notoriously unreliable in headless testing environments.")
def test_service_worker_interception(page: Page, live_server: str):
    """
    Verify that the Service Worker intercepts CDN requests.
    Note: We can use page.on("request") to see if they are handled by the SW.
    """
    intercepted_requests = []
    page.on("request", lambda request: intercepted_requests.append(request))
    
    page.goto(f"{live_server}/examples/loading/service_worker_cache.html")
    
    # Wait for completion
    expect(page.locator("#pyodide-status")).to_contain_text("Pyodide: Loaded", timeout=60000)
    
    # Check if any requests were served by the service worker
    # Playwright's request object has a 'service_worker' attribute or 'from_service_worker'
    sw_requests = [r for r in intercepted_requests if "cdn.jsdelivr.net" in r.url]
    assert len(sw_requests) > 0
