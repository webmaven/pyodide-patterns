from pyodide_app.bridge.reactivity import Signal


def test_signal_logic_in_cpython():
    """
    Verifies that the Signal class works correctly in CPython
    without any browser dependencies.
    """
    s = Signal[int](10)
    history = []

    s.subscribe(lambda v: history.append(v))
    assert s.value == 10
    assert history == [10]

    s.value = 20
    assert s.value == 20
    assert history == [10, 20]


def test_signal_type_safety():
    """Basic sanity check for generic Signal."""
    s = Signal[str]("hello")
    assert s.value == "hello"
