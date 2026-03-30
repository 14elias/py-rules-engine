from typing import Any


def get_nested(data: Any, path: str, default: Any = None) -> Any:
    """Safely access nested dictionary values using dot notation.

    Args:
        data: The data structure (usually a dict) to traverse.
        path: Dot-separated path (e.g. "profile.address.city").
        default: Value to return if the path does not exist or traversal fails.

    Returns:
        The value at the specified path, or `default` if not found.
    """

    if not isinstance(path, str):
        return default

    if not path:
        return data

    if not isinstance(data, dict):
        return data

    current = data
    for key in path.split("."):
        if not isinstance(current, dict):
            return default
        current = current.get(key, default)
    return current
