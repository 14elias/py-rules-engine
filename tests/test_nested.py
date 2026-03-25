from src.rules_engine.utils.nested import get_nested

def test_nested_access():
    data = {"a": {"b": {"c": 10}}}
    assert get_nested(data, "a.b.c") == 10


def test_missing_path():
    data = {"a": {}}
    assert get_nested(data, "a.b.c") is None