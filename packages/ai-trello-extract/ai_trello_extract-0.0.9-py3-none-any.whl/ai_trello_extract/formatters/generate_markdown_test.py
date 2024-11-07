from datetime import datetime
from typing import Literal
from unittest.mock import MagicMock

from ai_trello_extract.dataclasses.categorized_list import CategorizedLists
from ai_trello_extract.dataclasses.trello_card import TrelloCard

from .generate_markdown import format_label, generate_markdown


def test_headers():
    expected_markdown = """# BACKLOG

This is a list of cards, work items, user stories, and tasks that are in the backlog category.

# TODO

This is a list of cards, work items, user stories, and tasks that are in the todo category.

# DOING

This is a list of cards, work items, user stories, and tasks that are in the doing category.

# DONE

This is a list of cards, work items, user stories, and tasks that are in the done category.
"""

    categorized_list = CategorizedLists(
        backlog=[build_trello_card()],
        todo=[build_trello_card()],
        doing=[build_trello_card()],
        done=[build_trello_card()],
    )

    markdown = generate_markdown(categorized_list)

    assert markdown == expected_markdown


def test_card_title_names():
    expected_markdown = """# TODO

This is a list of cards, work items, user stories, and tasks that are in the todo category.

## Title: Title 1

## Title: Title 2
"""

    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(title="Title 1"),
            build_trello_card(title="Title 2"),
        ]
    )

    markdown = generate_markdown(categorized_list)

    assert markdown == expected_markdown


def test_card_list_names():
    expected_markdown = """# TODO

This is a list of cards, work items, user stories, and tasks that are in the todo category.

### List Name: List Name 1

### List Name: List Name 2
"""

    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(list_name="List Name 1"),
            build_trello_card(list_name="List Name 2"),
        ]
    )

    markdown = generate_markdown(categorized_list)

    assert markdown == expected_markdown


def test_card_labels():
    expected_markdown = """# TODO

This is a list of cards, work items, user stories, and tasks that are in the todo category.

### List Name: List Name 1

### Labels

- bug
- urgent
"""

    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(list_name="List Name 1", labels=["bug", "urgent"]),
        ]
    )

    markdown = generate_markdown(categorized_list)

    assert markdown == expected_markdown


def test_card_done_date():
    expected_markdown = """# TODO

This is a list of cards, work items, user stories, and tasks that are in the todo category.

### List Name: List Name 1

### Done Date: 2024-05-01 00:00:00
"""

    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(
                list_name="List Name 1",
                done_date=datetime(2024, 5, 1, 0, 0),
            ),
        ]
    )

    markdown = generate_markdown(categorized_list)

    assert markdown == expected_markdown


def test_card_descriptions():
    expected_markdown = """# TODO

This is a list of cards, work items, user stories, and tasks that are in the todo category.

### List Name: List Name 1

### Description

Description of task 1

### List Name: List Name 2

### Description

#### Description of task 2
"""

    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(list_name="List Name 1", description="Description of task 1"),
            build_trello_card(list_name="List Name 2", description="# Description of task 2"),
        ]
    )

    markdown = generate_markdown(categorized_list)

    assert markdown == expected_markdown


def test_card_comments():
    expected_markdown = """# TODO

This is a list of cards, work items, user stories, and tasks that are in the todo category.

### List Name: List Name 1

#### Comments

- - -

Comment 1
"""

    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(list_name="List Name 1", comments=["---", "Comment 1"]),
        ]
    )

    markdown = generate_markdown(categorized_list)

    assert markdown == expected_markdown


def test_generate_markdown():
    expected_markdown = """# TODO

This is a list of cards, work items, user stories, and tasks that are in the todo category.

## Title: Title 1

### List Name: List Name 1

### Labels

- bug
- urgent

### Done Date: 2024-05-01 00:00:00

### Description

Description of task 1

#### Comments

Comment 1
"""

    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(
                title="Title 1",
                list_name="List Name 1",
                labels=["bug", "urgent"],
                done_date=datetime(2024, 5, 1, 0, 0),
                description="Description of task 1",
                comments=["Comment 1"],
            ),
        ]
    )

    markdown = generate_markdown(categorized_list)

    assert markdown == expected_markdown


def test_format_label():
    label = MagicMock(id="12345")
    label.name = "Urgent"

    result = format_label(label)

    expected_output = """## Urgent
- **Label:** Urgent
- **Id:** 12345
"""
    assert result == expected_output


def build_trello_card(
    *,
    title="",
    list_name="",
    description="",
    labels: list[str] = [],
    comments: list[str] = [],
    done_date: datetime | Literal[""] = "",
) -> TrelloCard:
    return TrelloCard(
        title=title,
        list_name=list_name,
        description=description,
        labels=labels,
        comments=comments,
        done_date=done_date,
    )
