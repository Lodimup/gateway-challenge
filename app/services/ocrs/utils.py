import tiktoken


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string.
    See: https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
    Args:
        string (str): text string
        encoding_name (str): encoding name
    Returns:
        int: number of tokens
    """
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
