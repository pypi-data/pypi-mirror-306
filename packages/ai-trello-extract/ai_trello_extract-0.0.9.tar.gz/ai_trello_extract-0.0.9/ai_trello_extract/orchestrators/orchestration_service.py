import json
import os
from datetime import datetime
from itertools import groupby

from ai_trello_extract.formatters.generate_markdown import format_label, generate_markdown
from ai_trello_extract.services.trello_service import TrelloService


class OrchestrationService:
    def __init__(self, trello_service: TrelloService):
        self.trello_service = trello_service

    def add_card_to_board(self, board_name: str, card_name: str, card_description: str, labels: list[str]):
        self.trello_service.add_card_to_board(board_name, card_name, card_description, labels)

    def write_board_labels_to_file(self, board_name: str, directory: str) -> str:
        markdown_content = self.get_label_markdown(board_name)
        os.makedirs(directory, exist_ok=True)

        file_path = os.path.join(directory, f"{board_name} Trello Board Labels.txt")
        with open(file_path, "w") as file:
            file.write(markdown_content)
        return file_path

    def write_board_markdown_to_file(self, board_name: str, directory: str) -> str:
        markdown_content = self.get_board_markdown(board_name)
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, f"{board_name} Status Trello Board.txt")
        with open(file_path, "w") as file:
            file.write(markdown_content)
        return file_path

    def write_board_markdown_to_directory(self, board_name: str, directory: str) -> str:
        dir_path = os.path.join(directory, f"{board_name} Status Trello Board")
        os.makedirs(dir_path, exist_ok=True)

        markdown_content = self.get_board_markdown(board_name)
        transformed_markdown_content = self._extract_markdown_into_collections(markdown_content)

        for index, (title, content) in enumerate(transformed_markdown_content):
            index_str = f"{index:03}"
            file_path = os.path.join(dir_path, f"{index_str} {board_name} Trello Status {title}.txt")
            with open(file_path, "w") as file:
                file.write(content)

        return dir_path

    def _extract_markdown_into_collections(self, markdown_content: str) -> list[tuple[str, str]]:
        lines = markdown_content.split("\n")
        headers_and_content = self._extract_title_and_content(lines)
        return headers_and_content

    def _extract_title_and_content(self, lines):
        grouped_lines = groupby(lines, key=lambda line: line.startswith("# "))
        headers = [
            (header[2:], f"{datetime.now().strftime('%m-%d-%Y')}\n\n{header}\n" + "\n".join(content).strip())
            for is_header, group in grouped_lines
            if is_header
            for header in group
            for _, content in [next(grouped_lines, (False, []))]
        ]
        return headers

    def get_label_markdown(self, board_name: str) -> str:
        board = self.trello_service.get_board_by_name(board_name)
        labels = "\n".join([format_label(label) for label in board.get_labels()])

        return f"""# {board_name} Trello Board Labels

{labels}
"""

    def get_board_markdown(self, board_name: str) -> str:
        board = self.trello_service.get_board_by_name(board_name)
        return generate_markdown(self.trello_service.extract_cards_info(board))

    def write_board_json_to_file(self, board_name: str, directory: str) -> str:
        board_json = self.get_board_json(board_name)
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, f"{board_name} Trello.json")
        with open(file_path, "w") as file:
            json.dump(board_json, file, indent=2)
        return file_path

    def get_board_json(self, board_name: str) -> dict:
        board = self.trello_service.get_board_by_name(board_name)
        categorized_lists = self.trello_service.extract_cards_info(board)
        return categorized_lists.to_dict()
