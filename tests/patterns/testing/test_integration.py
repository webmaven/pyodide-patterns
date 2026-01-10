import sys
from unittest.mock import MagicMock, patch

# Mock the 'js' module *before* importing 'main'
sys.modules["js"] = MagicMock()

from pyodide_app.main import run  # noqa: E402
from pyodide_app.utils import format_greeting  # noqa: E402


@patch("pyodide_app.main.document")
def test_run_integration(mock_document):
    """
    An integration test to verify that 'main.run' correctly uses 'utils.format_greeting'
    to change the heading text.
    """
    mock_element = MagicMock()
    mock_document.getElementById.return_value = mock_element

    # Patch the 'format_greeting' function in the 'utils' module used by 'main'
    # This verifies the interaction between main and utils
    with patch("pyodide_app.main.utils.format_greeting", format_greeting):
        run()

    mock_document.getElementById.assert_called_once_with("title")
    assert mock_element.innerText == "Hello, World!"
