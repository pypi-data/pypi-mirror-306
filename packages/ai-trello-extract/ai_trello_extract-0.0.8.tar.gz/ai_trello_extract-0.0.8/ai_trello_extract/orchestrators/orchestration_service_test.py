import glob
import os
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

from trello import Board

from ai_trello_extract.dataclasses.categorized_list import CategorizedLists
from ai_trello_extract.dataclasses.trello_card import TrelloCard
from ai_trello_extract.services.trello_service import TrelloService

from .orchestration_service import OrchestrationService

expected_markdown = """# TODO

This is a list of cards, work items, user stories, and tasks that are in the todo category.

## Title: Title

### List Name: To Do

### Labels

- Label1
- Label2

### Done Date: 2024-01-01 00:00:00

### Description

Test card description

#### Comments

Test comment
"""


def test_get_board_markdown(mock_board: Board, trello_card: TrelloCard):
    mock_trello_service = MagicMock(spec=TrelloService)
    mock_trello_service.get_board_by_name.return_value = mock_board
    mock_trello_service.extract_cards_info.return_value = CategorizedLists(todo=[trello_card])

    orchestration_service = OrchestrationService(mock_trello_service)
    markdown = orchestration_service.get_board_markdown("Test Board")

    assert markdown == expected_markdown

    mock_trello_service.get_board_by_name.assert_called_once_with("Test Board")
    mock_trello_service.extract_cards_info.assert_called_once_with(mock_trello_service.get_board_by_name.return_value)


@patch("ai_trello_extract.orchestrators.orchestration_service.generate_markdown")
def test_write_board_markdown_to_file(mock_generate_markdown: MagicMock, tmpdir: Path):
    mock_generate_markdown.return_value = "# Mock Markdown Content"

    mock_trello_service = MagicMock(spec=TrelloService)
    mock_trello_service.get_board_by_name.return_value = "mock_board"
    mock_trello_service.extract_cards_info.return_value = "mock_cards_info"

    orchestration_service = OrchestrationService(trello_service=mock_trello_service)

    board_name = "TestBoard"
    directory = tmpdir.mkdir("markdown_files")
    file_path = os.path.join(directory, f"{board_name} Status Trello Board.txt")

    result_path = orchestration_service.write_board_markdown_to_file(board_name, str(directory))

    assert result_path == file_path
    with open(result_path, "r") as file:
        content = file.read()
    assert content == "# Mock Markdown Content"


@patch("ai_trello_extract.orchestrators.orchestration_service.generate_markdown")
def test_write_board_markdown_to_directory(mock_generate_markdown: MagicMock, tmpdir: Path):
    expected_date = datetime.now().strftime("%m-%d-%Y")

    first_contents = "# Mock Markdown Content\nSome other content"
    second_contents = "# New Header"
    mock_generate_markdown.return_value = f"{first_contents}\n{second_contents}"

    mock_trello_service = MagicMock(spec=TrelloService)
    mock_trello_service.get_board_by_name.return_value = "mock_board"
    mock_trello_service.extract_cards_info.return_value = "mock_cards_info"

    orchestration_service = OrchestrationService(trello_service=mock_trello_service)

    board_name = "TestBoard"
    directory = tmpdir.mkdir("markdown_files")

    base_path = f"{board_name} Status Trello Board"
    dir_path = os.path.join(directory, base_path)

    result_path = orchestration_service.write_board_markdown_to_directory(board_name, str(directory))

    assert result_path == dir_path
    assert os.path.basename(str(result_path)) == base_path

    first_file = glob.glob(os.path.join(str(dir_path), "*"))[0]

    with open(first_file, "r") as file:
        first_file_contents = file.read()
    assert first_file_contents == f"{expected_date}\n\n{first_contents}"

    second_file = glob.glob(os.path.join(str(dir_path), "*"))[1]

    with open(second_file, "r") as file:
        second_file_contents = file.read()
    assert second_file_contents == f"{expected_date}\n\n{second_contents}\n"


def test_write_board_json_to_file(tmpdir: Path):
    mock_trello_service = MagicMock(spec=TrelloService)
    mock_trello_service.get_board_by_name.return_value = "mock_board"
    mock_trello_service.extract_cards_info.return_value = MagicMock(to_dict=lambda: {})

    orchestration_service = OrchestrationService(trello_service=mock_trello_service)

    board_name = "TestBoard"
    directory = tmpdir.mkdir("markdown_files")
    file_path = os.path.join(directory, f"{board_name} Trello.json")

    result_path = orchestration_service.write_board_json_to_file(board_name, str(directory))

    assert result_path == file_path
    with open(result_path, "r") as file:
        content = file.read()
    assert content == "{}"


def test_get_board_json(mock_board: Board, trello_card: TrelloCard):
    expected_json = {
        "backlog": [],
        "todo": [
            {
                "title": "Title",
                "list_name": "To Do",
                "description": "Test card description",
                "labels": ["Label1", "Label2"],
                "comments": ["Test comment"],
                "done_date": "2024-01-01T00:00:00",
            }
        ],
        "doing": [],
        "done": [],
    }

    mock_trello_service = MagicMock(spec=TrelloService)
    mock_trello_service.get_board_by_name.return_value = mock_board
    mock_trello_service.extract_cards_info.return_value = CategorizedLists(todo=[trello_card])

    orchestration_service = OrchestrationService(mock_trello_service)
    board_json = orchestration_service.get_board_json("Test Board")

    assert board_json == expected_json

    mock_trello_service.get_board_by_name.assert_called_once_with("Test Board")
    mock_trello_service.extract_cards_info.assert_called_once_with(mock_trello_service.get_board_by_name.return_value)


def test_add_card_to_board():
    mock_trello_service = MagicMock(spec=TrelloService)
    orchestration_service = OrchestrationService(mock_trello_service)

    board_name = "Test Board"
    card_name = "Test Card"
    card_description = "This is a test card."

    orchestration_service.add_card_to_board(board_name, card_name, card_description)

    mock_trello_service.add_card_to_board.assert_called_once_with(board_name, card_name, card_description)


def test_write_board_labels_to_file(tmpdir: Path):
    mock_board = MagicMock(spec=Board)

    mock_trello_service = MagicMock(spec=TrelloService)
    mock_trello_service.get_board_by_name.return_value = mock_board

    mock_label = MagicMock(id="abc")
    mock_label.name = "Label1"

    mock_board.get_labels.return_value = [mock_label]

    orchestration_service = OrchestrationService(trello_service=mock_trello_service)

    board_name = "TestBoard"
    directory = tmpdir.mkdir("label_files")
    file_path = os.path.join(directory, f"{board_name} Trello Board Labels.txt")

    result_path = orchestration_service.write_board_labels_to_file(board_name, str(directory))

    assert result_path == file_path
    with open(result_path, "r") as file:
        content = file.read()
    expected_content = f"""# {board_name} Trello Board Labels

## Label1
- **Label:** Label1
- **Id:** abc

"""
    assert content == expected_content
