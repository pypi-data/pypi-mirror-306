from ai_trello_extract.env_variables import ENV_VARIABLES, set_env_variables


def test_reset_env_variables(tmp_path):
    """
    Test the set_env_variables function to ensure it correctly sets environment variables
    from a .env file.

    Args:
        tmp_path: pytest fixture that provides a temporary directory unique to the test invocation.
    """
    # Create a temporary .env file with test environment variables
    env_file = tmp_path / ".env"
    env_file.write_text(
        "TRELLO_API_KEY=test_api_key\n" "TRELLO_API_TOKEN=test_api_token\n" "TRELLO_BOARD_NAME=test_board_name\n"
    )

    # Call the function to set environment variables from the .env file
    set_env_variables(str(env_file))

    # Assert the environment variables are set correctly in the ENV_VARIABLES instance
    assert ENV_VARIABLES.trello_api_key == "test_api_key"
    assert ENV_VARIABLES.trello_api_token == "test_api_token"
    assert ENV_VARIABLES.trello_board_name == "test_board_name"
