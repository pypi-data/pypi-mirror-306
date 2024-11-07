from ai_trello_extract.formatters.escape_markdown import escape_markdown


def test_escape_markdown():
    """
    Test that escape_markdown correctly escapes markdown headers and horizontal rules.
    """
    input_text = """# Heading
Some text
---
Another line
## Another heading
---
### Final heading"""

    expected_output = """#### Heading
Some text
- - -
Another line
##### Another heading
- - -
###### Final heading"""

    # Verify that the function correctly escapes markdown headers and horizontal rules
    assert escape_markdown(input_text) == expected_output


def test_escape_markdown_max_heading_level():
    """
    Test that escape_markdown does not exceed the maximum heading level of 6.
    """
    input_text = "#### Heading"

    expected_output = "###### Heading"

    # Verify that the function correctly handles the maximum heading level
    assert escape_markdown(input_text) == expected_output
