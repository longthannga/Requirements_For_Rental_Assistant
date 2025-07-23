import tiktoken

def count_tokens(text: str, model_name: str = "gpt-3.5-turbo") -> int:
    """Count tokens in text using the specified encoding"""
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))