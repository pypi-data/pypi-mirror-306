from datetime import datetime
from unittest.mock import MagicMock

import pytest
from trello import Board, Card, Label, TrelloClient
from trello import List as TrelloList

from ai_trello_extract.dataclasses.trello_card import TrelloCard
from ai_trello_extract.services.trello_service import TrelloService


@pytest.fixture
def trello_service(mock_trello_client: TrelloClient) -> TrelloService:
    """
    Fixture to provide a TrelloService instance with a mocked Trello client.

    Args:
        mock_trello_client (TrelloClient): A mocked Trello client.

    Returns:
        TrelloService: An instance of TrelloService.
    """
    return TrelloService(client=mock_trello_client)


@pytest.fixture
def trello_card() -> TrelloCard:
    """
    Fixture to provide a TrelloCard instance with predefined attributes.

    Returns:
        TrelloCard: An instance of TrelloCard with predefined attributes.
    """
    return TrelloCard(
        title="Title",
        list_name="To Do",
        description="Test card description",
        labels=["Label1", "Label2"],
        comments=["Test comment"],
        done_date=datetime(2024, 1, 1, 0, 0, 0),
    )


@pytest.fixture
def mock_trello_client() -> MagicMock:
    """
    Fixture to provide a mocked Trello client.

    Returns:
        MagicMock: A mocked Trello client.
    """
    return MagicMock(spec=TrelloClient)


@pytest.fixture
def mock_board(mock_card: Card) -> MagicMock:
    """
    Fixture to provide a mocked Trello board with predefined lists and cards.

    Args:
        mock_card (Card): A mocked Trello card.

    Returns:
        MagicMock: A mocked Trello board.
    """

    def build_trello_list(list_name: str, mock_card: Card) -> MagicMock:
        trello_list = MagicMock(spec=TrelloList)
        trello_list.name = list_name
        trello_list.list_cards.return_value = [mock_card]
        return trello_list

    all_lists = [
        "Backlog",
        "Todo",
        "Doing",
        "Done",
        "Other",
        "_",
    ]

    board = MagicMock(spec=Board)
    board.name = "Test Board"
    board.all_lists.return_value = [build_trello_list(list_name, mock_card) for list_name in all_lists]
    return board


@pytest.fixture
def mock_trello_list() -> MagicMock:
    """
    Fixture to provide a mocked Trello list.

    Returns:
        MagicMock: A mocked Trello list.
    """
    mock_list = MagicMock(spec=TrelloList)
    mock_list.name = "Doing"
    return mock_list


@pytest.fixture
def mock_card() -> MagicMock:
    """
    Fixture to provide a mocked Trello card with predefined attributes.

    Returns:
        MagicMock: A mocked Trello card.
    """
    label_one = MagicMock(spec=Label)
    label_one.name = "Label1"
    label_two = MagicMock(spec=Label)
    label_two.name = "Label2"

    mock_card = MagicMock(spec=Card)
    mock_card.name = "Test Card"
    mock_card.description = "Test card description"
    mock_card.labels = [label_one, label_two]
    mock_card.comments = [{"data": {"text": "Test comment"}}]
    mock_card.due_date = datetime(2023, 1, 1)
    return mock_card
