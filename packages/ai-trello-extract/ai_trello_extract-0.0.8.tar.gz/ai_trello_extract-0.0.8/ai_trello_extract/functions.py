from typing import Iterator, Optional, TypeVar

T = TypeVar("T")


def first(iterable: Iterator[T], default: Optional[T] = None) -> Optional[T]:
    """
    Returns the first item from an iterator, or a default value if the iterator is empty.

    Args:
        iterable (Iterator[T]): The iterator to retrieve the first item from.
        default (Optional[T]): The default value to return if the iterator is empty.

    Returns:
        Optional[T]: The first item from the iterator, or the default value if the iterator is empty.
    """
    for item in iterable:
        return item
    return default
