import sys
import timeit

# Environment detection
IS_EMSCRIPTEN = sys.platform == "emscripten"

if IS_EMSCRIPTEN:
    from js import document
else:
    from unittest.mock import MagicMock

    document = MagicMock()

from . import utils  # noqa: E402


def change_heading_text(new_text: str) -> None:
    """Changes the text of the H1 element with id 'title'."""
    title_element = document.getElementById("title")
    if title_element:
        title_element.innerText = new_text
    else:
        print(f"Warning: Element with id 'title' not found. Text: {new_text}")


def add(a: int, b: int) -> int:
    """A pure logic function that adds two numbers."""
    return a + b


def greet(name: str) -> None:
    """Greets the user with the given name."""
    if not name:
        name = "World"
    greeting = utils.format_greeting(name)
    change_heading_text(greeting)


def run() -> None:
    """This function is called from the HTML file."""
    # Set an initial greeting
    greet("")


def benchmark_add() -> None:
    """Benchmarks the 'add' function and prints the result to the console."""
    execution_time = timeit.timeit("add(2, 3)", globals=globals(), number=100000)
    print(
        f"Execution time of 'add(2, 3)' (100,000 iterations): {execution_time} seconds"
    )
