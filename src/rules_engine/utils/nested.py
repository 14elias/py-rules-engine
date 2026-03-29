from typing import Any

def get_nested(data: Any, path: str, default: Any = None) -> Any:
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