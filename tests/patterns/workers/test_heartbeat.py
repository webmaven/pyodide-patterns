from playwright.sync_api import Page, expect

def test_worker_heartbeat_detection(page: Page, live_server: str):
    """
    Verify that the heartbeat pattern correctly identifies a hung worker.
    """
    page.goto(f"{live_server}/examples/loading/worker_heartbeat.html")
    
    # 1. Initially it should be alive
    status_box = page.locator("#status-box")
    expect(status_box).to_have_text("Worker Alive (Heartbeat OK)", timeout=30000)
    
    # 2. Trigger a silent crash (infinite loop)
    page.click("#btn-crash")
    
    # 3. Wait for the heartbeat timeout (configured for 5s in the example)
    # We use a 15s timeout here to be safe
    expect(status_box).to_have_text("Worker CRASHED or HUNG!", timeout=15000)
    
    log = page.locator("#log")
    expect(log).to_contain_text("FATAL: Heartbeat timeout. Worker is unresponsive.")
