from loguru import logger
from trello import Card
from trello import List as TrelloList

from ai_trello_extract.dataclasses.categorized_list import CategorizedLists
from ai_trello_extract.dataclasses.trello_card import TrelloCard


def extract_card_info(trello_list: TrelloList, card: Card) -> TrelloCard:
    """
    Extracts information from a Trello card and returns it as a TrelloCard dataclass.

    Args:
        trello_list (TrelloList): The Trello list containing the card.
        card (Card): The Trello card to extract information from.

    Returns:
        TrelloCard: A dataclass containing the extracted card information.
    """
    logger.debug(f"Extracting Trello Card information for card: {card.name}")
    return TrelloCard(
        list_name=trello_list.name,
        title=card.name,
        description=card.description,
        labels=[label.name for label in card.labels],
        comments=[comment["data"]["text"] for comment in card.comments],
        done_date=card.due_date,
    )


def trello_list_reducer(accumulator: CategorizedLists, trello_list: TrelloList) -> CategorizedLists:
    """
    Categorizes a Trello list into different categories and appends it to the appropriate list in the accumulator.

    Args:
        accumulator (CategorizedLists): The accumulator object that holds categorized Trello lists.
        trello_list (TrelloList): The Trello list to categorize.

    Returns:
        CategorizedLists: The updated accumulator with the Trello list categorized.
    """
    if trello_list.name in ["Backlog"]:
        accumulator.backlog.append(trello_list)
    elif trello_list.name in ["Todo"]:
        accumulator.todo.append(trello_list)
    elif trello_list.name in ["Doing"]:
        accumulator.doing.append(trello_list)
    elif trello_list.name in ["Done"]:
        accumulator.done.append(trello_list)
    else:
        pass

    return accumulator
