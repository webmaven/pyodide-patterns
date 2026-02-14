import time

from playwright.sync_api import Page, expect


def test_worker_pool_parallelism(page: Page, live_server: str):
    """
    Verify that the worker pool processes tasks in parallel.
    With 2 workers and 4 tasks of 2 seconds each:
    - Serial time: 8s
    - Parallel time: ~4s
    """
    page.goto(f"{live_server}/examples/workers/worker_pool.html")

    # Wait for initialization
    expect(page.locator("#status")).to_have_text(
        "Pool Ready. Running 2 workers.", timeout=60000
    )

    run_btn = page.locator("#run-batch-btn")
    expect(run_btn).to_be_enabled()

    start_time = time.time()
    run_btn.click()

    # Wait for completion message
    expect(page.locator("#status")).to_contain_text("Batch complete", timeout=30000)
    end_time = time.time()

    total_duration = end_time - start_time
    print(f"Pool Batch Duration: {total_duration:.2f}s")

    # Verify all tasks finished
    expect(page.locator(".task-log.success")).to_have_count(4)

    # Assert that it took significantly less than 8 seconds (the serial time)
    # 6s is a safe upper bound for a 4s parallel task in CI
    assert total_duration < 7.0, (
        f"Batch took too long ({total_duration:.2f}s), parallelism might be broken."
    )
    # It should take at least 4s
    assert total_duration >= 3.5
