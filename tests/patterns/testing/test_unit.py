from unittest.mock import MagicMock, patch

# Now we can import the app code directly
from pyodide_app.main import add, change_heading_text


def test_add():
    """Tests the pure logic 'add' function."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


@patch("pyodide_app.main.document")
def test_change_heading_text(mock_document):
    """Tests the 'change_heading_text' function with a mocked document."""
    mock_element = MagicMock()
    mock_document.getElementById.return_value = mock_element

    change_heading_text("New Text")

    mock_document.getElementById.assert_called_once_with("title")
    assert mock_element.innerText == "New Text"
