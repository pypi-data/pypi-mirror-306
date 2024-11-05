import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class EnvVariables:
    """
    Data class to store environment variables.
    """

    trello_api_key: str
    trello_api_token: str
    trello_board_name: str
    trello_board_add_column_name: str
    output_directory: str


def set_env_variables(env_file_path: str | None = None):
    """
    Load environment variables from a .env file and set them in the global ENV_VARIABLES instance.

    Args:
        env_file_path (str | None): Path to the .env file. If None, defaults to the .env file in the current directory.
    """
    global ENV_VARIABLES

    # Load environment variables from the specified .env file, overriding existing variables
    load_dotenv(env_file_path, override=True)

    # Set the environment variables in the global ENV_VARIABLES instance
    ENV_VARIABLES.trello_api_key = os.getenv("TRELLO_API_KEY", "Trello API Key")
    ENV_VARIABLES.trello_api_token = os.getenv("TRELLO_API_TOKEN", "Trello API Token")
    ENV_VARIABLES.trello_board_name = os.getenv("TRELLO_BOARD_NAME", "Trello Board Name")
    ENV_VARIABLES.trello_board_add_column_name = os.getenv("TRELLO_BOARD_ADD_COLUMN_NAME", "Icebox")
    ENV_VARIABLES.output_directory = os.getenv("OUTPUT_DIRECTORY", "output")


# Initialize the global ENV_VARIABLES instance with default values or values from the environment
ENV_VARIABLES = EnvVariables(
    trello_api_key=os.getenv("TRELLO_API_KEY", "Trello API Key"),
    trello_api_token=os.getenv("TRELLO_API_TOKEN", "Trello API Token"),
    trello_board_name=os.getenv("TRELLO_BOARD_NAME", "Trello Board Name"),
    trello_board_add_column_name=os.getenv("TRELLO_BOARD_ADD_COLUMN_NAME", "Icebox"),
    output_directory=os.getenv("OUTPUT_DIRECTORY", "output"),
)
