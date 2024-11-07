from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class CategorizedLists(Generic[T]):
    """
    A generic dataclass to categorize items into different lists.

    Attributes:
        backlog (list[T]): Items planned to be done.
        todo (list[T]): Items to be done.
        doing (list[T]): Items currently being worked on.
        done (list[T]): Items that have been completed.
    """

    backlog: list[T] = field(default_factory=list)
    todo: list[T] = field(default_factory=list)
    doing: list[T] = field(default_factory=list)
    done: list[T] = field(default_factory=list)

    def to_dict(self) -> dict:
        """
        Convert the CategorizedLists instance to a dictionary, serializing datetime objects.

        Returns:
            dict: A dictionary representation of the CategorizedLists instance.
        """

        def serialize(obj):
            # Convert datetime objects to ISO format strings
            if isinstance(obj, datetime):
                return obj.isoformat()
            return obj

        # Use asdict to convert the dataclass to a dictionary, applying the serialize function
        return asdict(self, dict_factory=lambda x: {k: serialize(v) for k, v in x})
