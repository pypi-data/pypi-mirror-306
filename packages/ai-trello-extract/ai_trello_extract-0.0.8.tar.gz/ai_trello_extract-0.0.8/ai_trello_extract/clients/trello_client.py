from trello import TrelloClient


def get_trello_client(trello_api_key: str, trello_api_token: str) -> TrelloClient:
    """
    Initialize and return a TrelloClient instance.

    Args:
        trello_api_key (str): The API key for Trello.
        trello_api_token (str): The API token for Trello.

    Returns:
        TrelloClient: An instance of TrelloClient initialized with the provided API key and token.
    """
    return TrelloClient(
        api_key=trello_api_key,
        api_secret=trello_api_token,
    )
