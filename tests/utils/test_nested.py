import pytest
from rules_engine.utils.nested import get_nested


def test_get_nested_basic_access():
    """Test basic nested dictionary access."""
    data = {"a": {"b": {"c": 10}}}
    assert get_nested(data, "a.b.c") == 10


def test_get_nested_missing_key_returns_default():
    """Test that missing keys return the provided default."""
    data = {"a": {"b": {}}}
    assert get_nested(data, "a.b.c") is None
    assert get_nested(data, "a.b.c", default="NOT_FOUND") == "NOT_FOUND"
    assert get_nested(data, "x.y.z", default=42) == 42


def test_get_nested_empty_path():
    """Test behavior when path is empty string."""
    data = {"a": 1}
    assert get_nested(data, "") is data
    assert get_nested(123, "") == 123  # even non-dict


def test_get_nested_non_dict_input():
    """Test when initial data is not a dictionary."""
    assert get_nested(10, "anything") == 10
    assert get_nested(None, "a.b") is None
    assert get_nested("string", "a.b") == "string"
    assert get_nested([1, 2, 3], "a.b") == [1, 2, 3]


def test_get_nested_path_goes_through_non_dict():
    """Test when a key in the middle of the path is not a dict."""
    data = {"a": {"b": 5}}  # b is int, not dict
    assert get_nested(data, "a.b.c") is None
    assert get_nested(data, "a.b.c", default="MISSING") == "MISSING"


def test_get_nested_with_none_values():
    """Test behavior when values in the path are None."""
    data = {"a": None}
    assert get_nested(data, "a") is None
    assert get_nested(data, "a.b") is None
    assert get_nested(data, "a.b", default="default") == "default"


def test_get_nested_empty_dict():
    """Test with empty dictionary."""
    assert get_nested({}, "a.b.c") is None
    assert get_nested({}, "a.b.c", default="empty") == "empty"


def test_get_nested_deep_nesting():
    """Test with very deep nesting."""
    data = {"a": {"b": {"c": {"d": {"e": 42}}}}}
    assert get_nested(data, "a.b.c.d.e") == 42
    assert get_nested(data, "a.b.c.d.e.f") is None


def test_get_nested_list_as_value():
    """Test when a value in the path is a list (should stop and return default)."""
    data = {"a": [1, 2, 3]}
    assert get_nested(data, "a.b") is None
    assert get_nested(data, "a.0") is None  # even though lists support indexing, we treat as non-dict


def test_get_nested_mixed_types():
    """Test various data types in the structure."""
    data = {
        "user": {
            "name": "Elias",
            "age": 30,
            "active": True,
            "scores": [95, 87, 91],
            "address": None,
        }
    }

    assert get_nested(data, "user.name") == "Elias"
    assert get_nested(data, "user.age") == 30
    assert get_nested(data, "user.active") is True
    assert get_nested(data, "user.scores") == [95, 87, 91]
    assert get_nested(data, "user.address") is None
    assert get_nested(data, "user.missing") is None
    assert get_nested(data, "user.scores.0") is None  # list treated as non-dict


def test_get_nested_invalid_path_types():
    """Test with non-string paths (should probably handle gracefully)."""
    data = {"a": 1}
    assert get_nested(data, None) is None  
    


@pytest.mark.parametrize(
    "data, path, default, expected",
    [
        ({"a": {"b": 10}}, "a.b", None, 10),
        ({"a": {"b": 10}}, "a.c", "missing", "missing"),
        ({}, "x.y", 999, 999),
        ({"a": 5}, "a.b", None, None),
        (123, "anything", "default", 123),
        (None, "a.b", "default", None),
        ({"a": {"b": {"c": None}}}, "a.b.c", "default", None),
    ],
)
def test_get_nested_parametrized(data, path, default, expected):
    """Parametrized test covering multiple scenarios."""
    assert get_nested(data, path, default) == expected