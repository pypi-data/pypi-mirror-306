from unittest.mock import MagicMock, patch

from ai_trello_extract.clients.trello_client import get_trello_client


@patch("ai_trello_extract.clients.trello_client.TrelloClient")
def test_get_trello_client(trello_client: MagicMock) -> None:
    """
    Test the get_trello_client function to ensure it initializes the TrelloClient correctly.

    Args:
        trello_client (MagicMock): Mocked TrelloClient class.
    """
    trello_api_key = "123"
    trello_api_token = "456"

    # Call the function to get the Trello client
    client = get_trello_client(trello_api_key, trello_api_token)

    # Verify that TrelloClient was called once with the correct arguments
    trello_client.assert_called_once_with(
        api_key=trello_api_key,
        api_secret=trello_api_token,
    )

    # Ensure the returned client is the mocked TrelloClient instance
    assert client == trello_client()
