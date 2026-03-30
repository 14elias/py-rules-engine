import pytest

from rules_engine import Field, Rule
from rules_engine.rules.contains import ContainsRule


@pytest.fixture
def sample_data():
    return {
        "age": 25,
        "country": "US",
        "name": "Abel",
        "tags": ["python", "ai", "ethiopia"],
        "scores": [10, 20, 30],
        "profile": {
            "email": "test@example.com",
            "hobbies": ["reading", "coding"],
            "empty_list": [],
            "none_value": None,
        },
        "bio": "Hello world",
        "empty_string": "",
        "single_tuple": (1, 2, 3),
        "nested_dict": {"key": "value"},
    }
# ====================== Basic Functionality ======================

def test_contains_success(sample_data):
    rule = Field("tags").contains("python")
    assert rule.evaluate(sample_data) is True


def test_contains_fail(sample_data):
    rule = Field("tags").contains("java")
    assert rule.evaluate(sample_data) is False


def test_contains_with_numbers(sample_data):
    rule = Field("scores").contains(20)
    assert rule.evaluate(sample_data) is True


def test_contains_empty_list(sample_data):
    rule = Field("profile.empty_list").contains("anything")
    assert rule.evaluate(sample_data) is False


def test_contains_in_tuple(sample_data):
    rule = Field("single_tuple").contains(2)
    assert rule.evaluate(sample_data) is True


def test_contains_in_string(sample_data):
    """Strings are iterable, so 'contains' should work on characters."""
    rule = Field("bio").contains("o")
    assert rule.evaluate(sample_data) is True

    rule2 = Field("bio").contains("Hello")
    assert rule2.evaluate(sample_data) is True


def test_contains_empty_string(sample_data):
    rule = Field("empty_string").contains("a")
    assert rule.evaluate(sample_data) is False


# ====================== Edge Cases & Failure Paths ======================

def test_contains_none_value(sample_data):
    """None collection should return False."""
    rule = Field("profile.none_value").contains("anything")
    assert rule.evaluate(sample_data) is False


def test_contains_missing_field(sample_data):
    """Missing field (get_nested returns None) → False."""
    rule = Field("non.existent.field").contains("python")
    assert rule.evaluate(sample_data) is False


def test_contains_non_iterable_int(sample_data):
    rule = Field("age").contains("python")
    assert rule.evaluate(sample_data) is False


def test_contains_non_iterable_bool():
    data = {"active": True}
    rule = Field("active").contains(True)
    assert rule.evaluate(data) is False


def test_contains_non_iterable_none():
    data = {"value": None}
    rule = Field("value").contains(123)
    assert rule.evaluate(data) is False


def test_contains_dict_as_collection(sample_data):
    """Dictionaries are iterable over keys."""
    rule = Field("nested_dict").contains("key")
    assert rule.evaluate(sample_data) is True

    rule2 = Field("nested_dict").contains("value")  # value is not a key
    assert rule2.evaluate(sample_data) is False


# ====================== TypeError Handling ======================

def test_contains_type_error_handling():
    """Objects that raise TypeError on 'in' check should return False."""
    class NonIterable:
        def __contains__(self, item):
            raise TypeError("Not iterable")

    data = {"bad": NonIterable()}
    rule = Field("bad").contains("anything")
    assert rule.evaluate(data) is False


# ====================== Serialization ======================

def test_contains_serialization_roundtrip(sample_data):
    original_rule = Field("tags").contains("python")

    d = original_rule.to_dict()
    assert d["type"] == "ContainsRule"
    assert d["field"] == "tags"
    assert d["value"] == "python"

    loaded = Rule.from_dict(d)
    assert isinstance(loaded, ContainsRule)
    assert loaded == original_rule
    assert loaded.evaluate(sample_data) is True


def test_contains_serialization_with_complex_value(sample_data):
    """Test serialization with non-primitive value (e.g. int, bool, list)."""
    rule = Field("scores").contains(20)
    loaded = Rule.from_dict(rule.to_dict())
    assert loaded.evaluate(sample_data) is True


# ====================== Equality & Repr ======================

def test_contains_equality():
    r1 = Field("tags").contains("python")
    r2 = Field("tags").contains("python")
    r3 = Field("tags").contains("java")

    assert r1 == r2
    assert r1 != r3
    assert r1 != "not a rule"


def test_contains_equality_with_different_types():
    r1 = Field("scores").contains(10)
    r2 = Field("scores").contains(10)
    r3 = Field("scores").contains("10")   # different type

    assert r1 == r2
    assert r1 != r3


def test_contains_repr(sample_data):
    rule = Field("profile.hobbies").contains("coding")
    repr_str = repr(rule)
    assert "Field('profile.hobbies')" in repr_str
    assert ".contains(" in repr_str
    assert "'coding'" in repr_str


# ====================== Parametrized Tests ======================

@pytest.mark.parametrize(
    "field, value, expected",
    [
        ("tags", "python", True),
        ("tags", "java", False),
        ("scores", 20, True),
        ("scores", 99, False),
        ("profile.empty_list", "x", False),
        ("bio", "world", True),
        ("bio", "xyz", False),
        ("age", 25, False),                    # non-iterable
        ("profile.none_value", None, False),
        ("non.existent", "anything", False),
        ("nested_dict", "key", True),
        ("single_tuple", 3, True),
    ],
)
def test_contains_parametrized(sample_data, field, value, expected):
    rule = Field(field).contains(value)
    assert rule.evaluate(sample_data) is expected