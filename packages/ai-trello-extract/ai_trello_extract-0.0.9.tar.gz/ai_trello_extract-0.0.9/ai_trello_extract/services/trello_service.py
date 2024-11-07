from functools import reduce

from loguru import logger
from trello import Board, Label, TrelloClient
from trello import List as TrelloList

from ai_trello_extract.dataclasses.categorized_list import CategorizedLists
from ai_trello_extract.dataclasses.trello_card import TrelloCard
from ai_trello_extract.env_variables import ENV_VARIABLES
from ai_trello_extract.functions import first

from .trello_utilities import extract_card_info, trello_list_reducer


def extract_card_info_from_list(trello_list: list[TrelloList]) -> list[TrelloCard]:
    return [extract_card_info(trello_list, card) for trello_list in trello_list for card in trello_list.list_cards()]


class TrelloService:
    def __init__(self, client: TrelloClient):
        self.client = client

    def add_card_to_board(self, board_name: str, card_name: str, card_description: str, labels: list[str]):
        board = self.get_board_by_name(board_name)

        board_list: list[TrelloList] = [
            column
            for column in self.get_lists_for_board(board)
            if column.name == ENV_VARIABLES.trello_board_add_column_name
        ]
        target_list = board_list[0] if board_list else None
        if not target_list:
            raise RuntimeError(f"No lists found on board '{board_name}'.")

        board_labels = self.get_labels_for_board(board)
        card_labels = [label for label in board_labels if label.name in labels]

        target_list.add_card(name=card_name, desc=card_description, labels=card_labels)

        logger.info(f"Card '{card_name}' added to list '{target_list.name}' on board '{board_name}'.")

    def get_labels_for_board(self, board: Board) -> list[Label]:
        logger.debug(f"Retrieving labels for board: {board.name}")
        return board.get_labels()

    def extract_cards_info(self, board: Board) -> CategorizedLists[TrelloCard]:
        categorized_lists = self.categorize_lists(board)

        logger.debug(f"Extracting Trello Cards from categorized lists: {categorized_lists}")

        planning = extract_card_info_from_list(categorized_lists.backlog)
        todo = extract_card_info_from_list(categorized_lists.todo)
        doing = extract_card_info_from_list(categorized_lists.doing)
        done = extract_card_info_from_list(categorized_lists.done)

        return CategorizedLists(backlog=planning, todo=todo, doing=doing, done=done)

    def categorize_lists(self, board: Board) -> CategorizedLists[TrelloList]:
        trello_lists = self.get_lists_for_board(board)
        filtered_trello_lists = filter(lambda trello_list: "_" != trello_list.name, trello_lists)
        return reduce(
            trello_list_reducer,
            filtered_trello_lists,
            CategorizedLists[TrelloList](backlog=[], todo=[], doing=[], done=[]),
        )

    def get_board_by_name(self, board_name: str) -> Board:
        boards = self._list_boards()
        board = first(filter(lambda board: board.name == board_name, boards))

        if not board:
            raise RuntimeError(f"Board with name '{board_name}' not found.")

        return board

    def get_lists_for_board(self, board: Board) -> list[TrelloList]:
        logger.debug(f"Listing Trello Lists for board: {board.name}")
        return board.all_lists()

    def _list_boards(self) -> list[Board]:
        logger.debug("Listing Trello Boards")
        return self.client.list_boards()
