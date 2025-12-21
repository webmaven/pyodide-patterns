import pytest
from playwright.sync_api import Page, expect
import time

def test_benchmark_button(page: Page, http_server):
    """
    A performance test using Playwright to verify that the benchmark button
    prints the benchmark result to the console.
    """
    logs = []
    page.on("console", lambda msg: logs.append(msg.text))

    page.goto(f"{http_server}/index.html")

    # Wait for Pyodide to initialize
    expect(page.locator("#title")).to_have_text("Hello, World!", timeout=10000)

    # Find the benchmark button and click it
    benchmark_button = page.locator("#benchmark-button")
    benchmark_button.click()

    # Wait for the benchmark result to be printed to the console
    # We're looking for a message that starts with "Execution time"
    # We'll need to poll the logs for a bit.
    timeout = time.time() + 10 # 10 second timeout
    benchmark_result = None
    while time.time() < timeout:
        for log in logs:
            if "Execution time" in log:
                benchmark_result = log
                break
        if benchmark_result:
            break
        time.sleep(0.1)

    assert benchmark_result is not None, "Benchmark result not found in console logs"
    print(f"\nBenchmark Result: {benchmark_result}")
