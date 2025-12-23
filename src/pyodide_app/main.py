import timeit

from js import document

from . import utils


def change_heading_text(new_text):
    """Changes the text of the H1 element with id 'title'."""
    title_element = document.getElementById("title")
    title_element.innerText = new_text

def add(a, b):
    """A pure logic function that adds two numbers."""
    return a + b

def greet(name):
    """Greets the user with the given name."""
    if not name:
        name = "World"
    greeting = utils.format_greeting(name)
    change_heading_text(greeting)

def run():
    """This function is called from the HTML file."""
    # Set an initial greeting
    greet("")

def benchmark_add():
    """Benchmarks the 'add' function and prints the result to the console."""
    execution_time = timeit.timeit("add(2, 3)", globals=globals(), number=100000)
    print(f"Execution time of 'add(2, 3)' (100,000 iterations): {execution_time} seconds")
