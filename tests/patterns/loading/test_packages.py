import pytest
from playwright.sync_api import Page, expect


def wait_for_pyodide(page: Page, timeout=30000):
    """A helper function to wait until Pyodide is loaded and ready."""
    expect(page.locator("#status")).to_have_text(
        "Pyodide loaded. Ready.", timeout=timeout
    )


def test_load_package_happy_path(page: Page, live_server: str):
    """
    Tests the 'happy path' for pyodide.loadPackage() with a bundled package.
    """
    page.goto(f"{live_server}/examples/loading/load_package.html")
    wait_for_pyodide(page)

    success = page.evaluate("async () => await loadPkg('numpy')")
    assert success is True

    result = page.evaluate(
        "window.pyodide.runPython('import numpy; numpy.array([1, 2, 3]).sum().item()')"
    )
    assert result == 6


def test_load_package_not_found(page: Page, live_server: str):
    """
    Tests that pyodide.loadPackage() fails when given a non-existent package.
    """
    page.goto(f"{live_server}/examples/loading/load_package.html")
    wait_for_pyodide(page)

    success = page.evaluate(
        "async () => await loadPkg('a-package-that-does-not-exist')"
    )
    assert success is False

    expect(page.locator("#status")).to_contain_text(
        "No known package with name 'a-package-that-does-not-exist'"
    )


def test_load_package_no_dependency_resolution(page: Page, live_server: str):
    """
    Tests that pyodide.loadPackage() from a URL does not handle dependencies.
    """
    page.goto(f"{live_server}/examples/loading/load_package.html")
    wait_for_pyodide(page)

    # Use the pyodide_patterns wheel which is available
    wheel_url = f"{live_server}/dist/pyodide_patterns-0.1.0-py3-none-any.whl"
    success = page.evaluate(f"async () => await loadPkg('{wheel_url}')")
    assert success is True

    # This test confirms that `loadPackage` does not resolve dependencies.
    result = page.evaluate(
        "window.pyodide.runPython("
        "'import pyodide_app; pyodide_app.main.run()')"
    )
    assert result is None

    with pytest.raises(Exception) as e:
        page.evaluate("window.pyodide.runPython('import tinycss2')")

    assert "ModuleNotFoundError" in str(e.value)


def test_load_from_imports_happy_path(page: Page, live_server: str):
    """
    Tests the 'happy path' for pyodide.loadPackagesFromImports() with a bundled package.
    """
    page.goto(f"{live_server}/examples/loading/load_from_imports.html")
    wait_for_pyodide(page)

    python_code = "import numpy; print('numpy imported')"
    # Use backticks (template literals) in JS to avoid quote conflicts
    success = page.evaluate(f"async () => await loadFromImports(`{python_code}`)")
    assert success is True

    result = page.evaluate(
        "window.pyodide.runPython('numpy.array([1, 2, 3]).sum().item()')"
    )
    assert result == 6


def test_load_from_imports_pypi_failure(page: Page, live_server: str):
    """
    Tests that pyodide.loadPackagesFromImports() fails to load packages from PyPI.
    """
    page.goto(f"{live_server}/examples/loading/load_from_imports.html")
    wait_for_pyodide(page)

    python_code = "import tinycss2; print('tinycss2 imported')"
    success = page.evaluate(f"async () => await loadFromImports(`{python_code}`)")
    assert success is False

    expect(page.locator("#status")).to_contain_text("ModuleNotFoundError")


def test_micropip_install_from_pypi(page: Page, live_server: str):
    """
    Tests the 'happy path' for micropip.install() from PyPI.
    """
    page.goto(f"{live_server}/examples/loading/micropip_install.html")
    expect(page.locator("#status")).to_have_text(
        "Pyodide and micropip loaded. Ready.", timeout=60000
    )

    success = page.evaluate("async () => await installPkg('tinycss2')")
    assert success is True

    # Verify the package is usable
    result = page.evaluate(
        "window.pyodide.runPython('import tinycss2; tinycss2.__version__')"
    )
    assert isinstance(result, str)


def test_micropip_install_from_url_with_deps(page: Page, live_server: str):
    """
    Tests micropip.install() from a URL, ensuring dependencies are also resolved.
    """
    page.goto(f"{live_server}/examples/loading/micropip_install.html")
    expect(page.locator("#status")).to_have_text(
        "Pyodide and micropip loaded. Ready.", timeout=60000
    )

    wheel_url = (
        f"{live_server}/_my_local_package/dist/my_local_package-0.1.0-py3-none-any.whl"
    )
    success = page.evaluate(f"async () => await installPkg('{wheel_url}')")
    assert success is True

    # Verify both the package and its dependency are usable
    result_pkg = page.evaluate(
        "window.pyodide.runPython("
        "'import my_local_package; my_local_package.a_test_function()')"
    )
    assert result_pkg == "This is from my_local_package"
    result_dep = page.evaluate(
        "window.pyodide.runPython('import tinycss2; tinycss2.__version__')"
    )
    assert isinstance(result_dep, str)


def test_micropip_install_404_failure(page: Page, live_server: str):
    """
    Tests that micropip.install() fails correctly when given a 404 URL.
    """
    page.goto(f"{live_server}/examples/loading/micropip_install.html")
    expect(page.locator("#status")).to_have_text(
        "Pyodide and micropip loaded. Ready.", timeout=60000
    )

    # Use a valid wheel filename format, even though the file doesn't exist.
    wheel_url = f"{live_server}/non_existent_package-1.0-py3-none-any.whl"
    success = page.evaluate(f"async () => await installPkg('{wheel_url}')")
    assert success is False
    wheel_url = f"{live_server}/non_existent_package-1.0-py3-none-any.whl"
    success = page.evaluate(f"async () => await installPkg('{wheel_url}')")
    assert success is False
    # Verify the error message indicates a BadZipFile (the content is HTML, not a wheel)
    expect(page.locator("#status")).to_contain_text("zipfile.BadZipFile")


def test_micropip_install_cors_failure_new(
    page: Page, live_server: str, cross_origin_server: str
):
    """
    Tests that micropip.install() fails with a CORS error when the server
    does not send CORS headers.
    """
    page.goto(f"{live_server}/examples/loading/micropip_install.html")
    expect(page.locator("#status")).to_have_text(
        "Pyodide and micropip loaded. Ready.", timeout=60000
    )
    # The wheel is hosted on a server without CORS headers
    wheel_url = f"{cross_origin_server}/dist/pyodide_patterns-0.1.0-py3-none-any.whl"
    # Expect a console error about CORS
    with page.expect_console_message(
        lambda msg: "Access-Control-Allow-Origin" in msg.text
    ):
        success = page.evaluate(f"async () => await installPkg('{wheel_url}')")
        assert success is False
    expect(page.locator("#status")).to_contain_text("Failed to install")
