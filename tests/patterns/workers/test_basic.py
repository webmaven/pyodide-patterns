# This file will contain tests for Pyodide running in a Web Worker.

from playwright.sync_api import Page, expect


def test_pyodide_in_worker_happy_path(page: Page, live_server: str):
    """
    The 'happy path' for Pyodide in a Web Worker.

    It loads a page that starts a worker, which in turn loads Pyodide
    and runs a simple Python script. The test asserts that the success
    message is posted back to the main thread.
    """
    page.goto(f"{live_server}/examples/workers/pyodide_worker.html")

    # The worker should post a message back with the Python version.
    status_element = page.locator("#status")

    # Wait for the success message, allowing a long timeout for Pyodide to load.
    expect(status_element).to_contain_text("Python script successful!", timeout=60000)


def test_python_error_in_worker(page: Page, live_server: str):
    """
    Tests the scenario where a Python script inside a worker fails.

    The key to this test is that the worker script itself must be written
    to catch the Python exception and post it back to the main thread.
    This test asserts that the error message is correctly displayed.
    """
    page.goto(f"{live_server}/examples/workers/pyodide_worker_error.html")

    status_element = page.locator("#status")

    # Wait for the error message to be displayed.
    expect(status_element).to_contain_text("Worker caught Python error", timeout=60000)
    expect(status_element).to_contain_text(
        "ZeroDivisionError: division by zero",
        timeout=1000,  # Should be quick after the first check
    )


# def test_worker_script_fails_to_load(page: Page, live_server: str):
#     """
#     NOTE: This test is commented out because it represents a known
#     difficult testing scenario that does not currently have a reliable solution.
#
#     The goal is to detect when a worker script itself fails to load (e.g., a 404).
#     While the browser's devtools and the test runner's stderr clearly show a 404
#     network request for the worker's script, capturing this event in Playwright
#     has proven to be unreliable.
#
#     Approaches tried and failed:
#     1. `page.on("requestfailed")`: Does not fire for the worker's
#        initial script request.
#     2. `page.expect_console_message()`: The browser does not consistently log a
#        console message for this failure that can be reliably caught by the test.
#     3. `worker.on("error")`: The `worker` object is never created, so no error
#        event can be listened for.
#     4. `page.on("response")`: This also does not seem to fire for the worker's
#        initial script request, even though other resources trigger it.
#
#     This test is preserved as a valuable example of a "mysterious" failure
#     and a known limitation in testability.
#     """
#     response_event = threading.Event()
#     failed_response = None
#
#     def on_response(response):
#         if (
#             "a_worker_that_does_not_exist.js" in response.url
#             and response.status == 404
#         ):
#             failed_response = response
#             response_event.set()
#
#     page.on("response", on_response)
#     page.goto(f"{live_server}/worker_load_error.html")
#
#     event_fired = response_event.wait(timeout=10)
#
#     assert event_fired, "Did not capture a 404 response for the worker script."
#     assert failed_response is not None
