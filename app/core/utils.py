import json

def normalize_value(value) -> str:
    """ Normalize Python dict values to JSON values before encryption. 
    Args:
        value: The value to normalize.
    Returns:
        The normalized string representation of the value."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, str):
        return value
    return json.dumps(value)