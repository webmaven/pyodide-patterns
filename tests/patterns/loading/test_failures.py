from playwright.sync_api import Page, expect


def test_pyodide_loads_successfully(page: Page, live_server: str):
    """
    The 'happy path' test for loading Pyodide.

    It navigates to a page that loads the Pyodide runtime and asserts that
    the `pyodide` object is attached to the window, confirming a successful load.
    """
    console_logs = []
    page.on("console", lambda msg: console_logs.append(msg.text))
    page.on("pageerror", lambda exc: console_logs.append(f"Page Error: {exc}"))

    page.goto(f"{live_server}/examples/hello_world.html")

    # Wait for Pyodide to be attached to the window
    try:
        page.wait_for_function("!!window.pyodide", timeout=60000)
    except Exception:
        print("\nBrowser Console Logs:")
        for log in console_logs:
            print(log)
        raise

    # Check that the pyodide object is on the window
    pyodide_on_window = page.evaluate("!!window.pyodide")
    assert pyodide_on_window is True


def test_pyodide_fails_to_load(page: Page, live_server: str):
    """
    Tests the scenario where the Pyodide runtime itself fails to load.

    It navigates to a page with a bad URL for `pyodide.js`, confirms that
    the script request failed, and asserts that the `pyodide` object
    is not attached to the window.
    """
    failed_requests = []
    page.on("requestfailed", lambda request: failed_requests.append(request))

    page.goto(f"{live_server}/examples/loading/load_error.html")

    # Wait for the page to indicate that the load failed.
    expect(page.locator("p")).to_have_text("Pyodide failed to load, as expected.")

    # Find the failed request for our script
    failed_script_request = None
    for req in failed_requests:
        if "a_file_that_does_not_exist.js" in req.url:
            failed_script_request = req
            break

    assert failed_script_request is not None, (
        "Did not find the failed request for the Pyodide script."
    )

    # Check that the pyodide object is NOT on the window
    pyodide_on_window = page.evaluate("!!window.pyodide")
    assert pyodide_on_window is False


def test_micropip_fails_to_install_package(page: Page, live_server: str):
    """
    Tests the scenario where micropip fails to install a non-existent package.

    It navigates to a page that runs a Python script to install a bad package
    and asserts that the expected Python error is logged to the console.
    """
    console_messages = []
    page.on("console", lambda msg: console_messages.append(msg.text))

    page.goto(f"{live_server}/examples/loading/micropip_fail.html")

    # Wait for the page to indicate that the install failed.
    expect(page.locator("p")).to_have_text(
        "Micropip failed to install, as expected.", timeout=30000
    )

    # Check the console for the specific Python error message
    log_text = "".join(console_messages)
    # Different versions of Pyodide/micropip may return different error messages
    possible_errors = [
        "ValueError: Can't fetch metadata",
        "ValueError: Unsupported content type"
    ]
    assert any(error in log_text for error in possible_errors), (
        f"Expected one of {possible_errors} in console logs, but got: {log_text}"
    )


def test_python_runtime_error(page: Page, live_server: str):
    """
    Tests the scenario where a Python script fails with a runtime error.

    It navigates to a page that runs a Python script with a ZeroDivisionError
    and asserts that the correct Python traceback is logged to the console.
    """
    console_messages = []
    page.on("console", lambda msg: console_messages.append(msg.text))

    page.goto(f"{live_server}/examples/loading/runtime_error.html")

    # Wait for the page to indicate that the script failed.
    expect(page.locator("p")).to_have_text(
        "Python script failed, as expected.", timeout=30000
    )

    # Check the console for the specific Python error message
    log_text = "".join(console_messages)
    assert "ZeroDivisionError: division by zero" in log_text
