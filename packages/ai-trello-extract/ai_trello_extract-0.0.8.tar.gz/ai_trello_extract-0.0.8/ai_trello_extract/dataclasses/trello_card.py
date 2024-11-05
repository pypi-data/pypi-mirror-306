from dataclasses import dataclass
from datetime import datetime
from typing import List, Literal


@dataclass
class TrelloCard:
    """
    A dataclass representing a Trello card.

    Attributes:
        title (str): The title of the Trello card.
        list_name (str): The name of the list the card belongs to.
        description (str): The description of the Trello card.
        labels (List[str]): A list of labels associated with the card.
        comments (List[str]): A list of comments on the card.
        done_date (datetime | Literal[""]): The date the card was marked as done, or an empty string if not done.
    """

    title: str
    list_name: str
    description: str
    labels: List[str]
    comments: List[str]
    done_date: datetime | Literal[""]
