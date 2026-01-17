# This file will contain tests for advanced Pyodide and Web Worker scenarios.
from playwright.sync_api import Page, expect


def wait_for_worker_ready(page: Page, timeout=60000):
    """Waits for the worker to initialize Pyodide and micropip."""
    expect(page.locator("#status")).to_have_text(
        "Pyodide and micropip ready.", timeout=timeout
    )


def test_micropip_in_worker_happy_path(page: Page, live_server: str):
    """
    Tests the 'happy path' of installing a package with micropip inside a worker.
    """
    page.goto(f"{live_server}/examples/workers/package_loading.html")
    wait_for_worker_ready(page)

    # Tell the worker to install a real package
    page.evaluate("installPackageInWorker('tinycss2')")

    # Assert that the success message is eventually posted back
    expect(page.locator("#success-tinycss2")).to_be_visible(timeout=30000)


def test_micropip_in_worker_package_not_found(page: Page, live_server: str):
    """
    Tests that a micropip 'PackageNotFoundError' inside a worker is correctly
    caught and propagated back to the main thread.
    """
    page.goto(f"{live_server}/examples/workers/package_loading.html")
    wait_for_worker_ready(page)

    # Tell the worker to install a non-existent package
    page.evaluate("installPackageInWorker('a-package-that-will-never-exist')")

    # Assert that the specific Python error is displayed on the page
    status_element = page.locator("#status")
    expect(status_element).to_contain_text(
        "Can't fetch metadata for 'a-package-that-will-never-exist'", timeout=30000
    )


def test_micropip_in_worker_cors_failure(
    page: Page, live_server: str, cross_origin_server: str
):
    """
    Tests that a CORS error when installing a package inside a worker is
    correctly caught and propagated.
    """
    page.goto(f"{live_server}/examples/workers/package_loading.html")
    wait_for_worker_ready(page)

    # This URL is on a server that does NOT send CORS headers
    wheel_url = (
        f"{cross_origin_server}/_my_local_package/dist/"
        "my_local_package-0.1.0-py3-none-any.whl"
    )

    # Tell the worker to install the package from the cross-origin URL
    page.evaluate(f"installPackageInWorker('{wheel_url}')")

    # Assert that the specific JavaScript network error is displayed on the page
    status_element = page.locator("#status")
    expect(status_element).to_contain_text("Failed to fetch", timeout=30000)


def test_dataclone_error_when_posting_pyproxy_to_worker(page: Page, live_server: str):
    """
    Tests for the 'DataCloneError' that occurs when trying to post a
    Pyodide PyProxy object from the main thread to a worker.
    """
    page.goto(f"{live_server}/examples/workers/dataclone_error.html")

    # The JavaScript on the page will catch the error and update the status.
    status_element = page.locator("#status")

    # Assert that the page correctly identifies the DataCloneError.
    expect(status_element).to_have_text(
        "Caught expected error: DataCloneError",
        timeout=60000,  # Pyodide load can be slow
    )
