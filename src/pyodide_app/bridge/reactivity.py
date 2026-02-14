from typing import Any, Callable, Generic, List, TypeVar

T = TypeVar("T")

# --- Reactive Signals ---


class Signal(Generic[T]):
    """A fine-grained reactive signal."""

    def __init__(self, value: T):
        self._value: T = value
        self._subscribers: List[Callable[[T], None]] = []

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, new_value: T):
        self._value = new_value
        self._notify()

    def subscribe(self, callback: Callable[[T], None]) -> None:
        self._subscribers.append(callback)
        callback(self._value)

    def _notify(self) -> None:
        for cb in self._subscribers:
            cb(self._value)


# --- Observable Dataclasses ---


def observable(cls: Any) -> Any:
    """Decorator that adds subscription capabilities to a class."""
    orig_init = cls.__init__

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: N807
        object.__setattr__(self, "_subscribers", {})
        orig_init(self, *args, **kwargs)

    def subscribe(self, field_name: str, callback: Callable[[Any], None]) -> None:
        if field_name not in self._subscribers:
            self._subscribers[field_name] = []
        self._subscribers[field_name].append(callback)
        callback(getattr(self, field_name))

    def __setattr__(self, name: str, value: Any) -> None:  # noqa: N807
        object.__setattr__(self, name, value)
        if hasattr(self, "_subscribers") and name in self._subscribers:
            for cb in self._subscribers[name]:
                cb(value)

    cls.__init__ = __init__
    cls.subscribe = subscribe
    cls.__setattr__ = __setattr__
    return cls
