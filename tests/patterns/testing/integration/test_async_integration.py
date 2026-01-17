import pytest
from unittest.mock import MagicMock, patch
import asyncio

# The 'js' and 'pyodide' modules are already mocked in conftest.py
import js

# Import from the source package
from pyodide_app.main import run

@pytest.mark.asyncio
async def test_run_async_integration():
    """
    An async integration test that verifies 'main.run' in an isolated environment.
    This test runs successfully because it is isolated from the Playwright test suite.
    """
    # Simulate some async work
    await asyncio.sleep(0.01)

    with patch("pyodide_app.main.document") as mock_document:
        mock_element = MagicMock()
        mock_document.getElementById.return_value = mock_element

        run()

        mock_document.getElementById.assert_called_once_with("title")
        assert mock_element.innerText == "Hello, World!"

async def mock_pyfetch(url):
    mock_response = MagicMock()

    async def mock_bytes():
        return MagicMock(to_py=lambda: b"fake-data")

    mock_response.bytes = mock_bytes
    return mock_response

@pytest.mark.asyncio
async def test_async_fetch_simulation():
    """
    Demonstrates an async test that simulates a network fetch,
    similar to how real Pyodide apps might work.
    """
    with patch("js.pyfetch", side_effect=mock_pyfetch):
        response = await js.pyfetch("test.data")
        data_proxy = await response.bytes()
        data = data_proxy.to_py()
        assert data == b"fake-data"
