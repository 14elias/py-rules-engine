import pytest

from rules_engine import Field, Rule
from rules_engine.rules.comparison import ComparisonRule


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

# ====================== Basic Comparisons ======================

def test_greater_than(sample_data):
    rule = Field("age") > 20
    assert rule.evaluate(sample_data) is True


def test_greater_than_or_equal(sample_data):
    rule = Field("age") >= 25
    assert rule.evaluate(sample_data) is True


def test_less_than(sample_data):
    rule = Field("age") < 30
    assert rule.evaluate(sample_data) is True


def test_less_than_or_equal(sample_data):
    rule = Field("age") <= 25
    assert rule.evaluate(sample_data) is True


def test_equal(sample_data):
    rule = Field("country") == "US"
    assert rule.evaluate(sample_data) is True


def test_not_equal(sample_data):
    rule = Field("country") != "UK"
    assert rule.evaluate(sample_data) is True


def test_equal_with_string(sample_data):
    rule = Field("name") == "Abel"
    assert rule.evaluate(sample_data) is True


# ====================== Edge Cases ======================

def test_comparison_missing_field(sample_data):
    rule = Field("non.existent.field") == 100
    assert rule.evaluate(sample_data) is False


def test_comparison_field_is_none(sample_data):
    rule = Field("profile.none_value") == 10
    assert rule.evaluate(sample_data) is False


def test_comparison_type_mismatch(sample_data):
    """Different types should return False (as per your implementation)."""
    rule1 = Field("age") > "25"          # int vs str
    rule2 = Field("name") == 123         # str vs int
    rule3 = Field("age") == "25"         # int vs str

    assert rule1.evaluate(sample_data) is False
    assert rule2.evaluate(sample_data) is False
    assert rule3.evaluate(sample_data) is False


def test_comparison_with_none_value(sample_data):
    """None in data should return False."""
    rule = Field("profile.none_value") > 0
    assert rule.evaluate(sample_data) is False


def test_comparison_empty_string(sample_data):
    rule = Field("empty_string") == ""
    assert rule.evaluate(sample_data) is True

    rule2 = Field("empty_string") != "hello"
    assert rule2.evaluate(sample_data) is True


# ====================== Unsupported Operator ======================

def test_unsupported_operator_raises(sample_data):
    """Unknown operator should raise ValueError (as implemented)."""
    rule = ComparisonRule(field_name="age", operator="~~", value=10)

    with pytest.raises(ValueError, match="Unknown operator"):
        rule.evaluate(sample_data)


# ====================== Serialization ======================

def test_comparison_serialization_roundtrip(sample_data):
    original = Field("age") >= 25

    d = original.to_dict()
    assert d["type"] == "ComparisonRule"
    assert d["field"] == "age"
    assert d["op"] == ">="
    assert d["value"] == 25

    loaded = Rule.from_dict(d)
    assert isinstance(loaded, ComparisonRule)
    assert loaded == original
    assert loaded.evaluate(sample_data) is True


def test_comparison_serialization_string(sample_data):
    original = Field("country") == "US"
    loaded = Rule.from_dict(original.to_dict())

    assert loaded.evaluate(sample_data) is True


# ====================== Equality & Repr ======================

def test_comparison_equality():
    r1 = Field("age") == 25
    r2 = Field("age") == 25
    r3 = Field("age") == 30

    assert r1 == r2
    assert r1 != r3
    assert r1 != "not a rule"


def test_comparison_equality_different_operators():
    r1 = Field("age") > 20
    r2 = Field("age") >= 20
    assert r1 != r2


def test_comparison_repr(sample_data):
    rule = Field("age") > 18
    repr_str = repr(rule)
    assert "Field('age')" in repr_str
    assert "> 18" in repr_str


# ====================== Parametrized Tests ======================

@pytest.mark.parametrize(
    "field, operator, value, expected",
    [
        ("age", "==", 25, True),
        ("age", "!=", 30, True),
        ("age", ">", 20, True),
        ("age", ">=", 25, True),
        ("age", "<", 30, True),
        ("age", "<=", 25, True),
        ("country", "==", "US", True),
        ("country", "!=", "ET", True),
        ("name", "==", "Abel", True),
        ("scores", "==", [10, 20, 30], True),   
        ("profile.none_value", "==", None, False),
        ("empty_string", "==", "", True),
        ("missing.field", ">", 10, False),
    ],
)
def test_comparison_parametrized(sample_data, field, operator, value, expected):
    rule = ComparisonRule(field_name=field, operator=operator, value=value)
    assert rule.evaluate(sample_data) is expected