def escape_markdown(text: str) -> str:
    """
    Escapes markdown in the given text by processing each line individually.

    Args:
        text (str): The input text containing markdown.

    Returns:
        str: The text with escaped markdown.
    """
    # Split the text into lines, escape each line, and join them back with newline characters
    return "\n".join(map(escape_line, text.split("\n")))


def escape_line(line: str) -> str:
    """
    Escapes specific markdown patterns in a single line of text.

    Args:
        line (str): A single line of text.

    Returns:
        str: The line with escaped markdown.
    """
    # If the line starts with one or more '#' characters, increase the number of '#' characters
    # to avoid it being interpreted as a header in markdown
    if line.startswith("#"):
        num_hashes = len(line) - len(line.lstrip("#"))
        num_hashes = min(num_hashes + 3, 6)  # Ensure the number of '#' does not exceed 6
        return "#" * num_hashes + line.lstrip("#")

    # If the line is exactly "---", replace it with "- - -" to avoid it being interpreted as a horizontal rule
    if line.strip() == "---":
        return "- - -"

    # Return the line unchanged if no special markdown patterns are found
    return line
