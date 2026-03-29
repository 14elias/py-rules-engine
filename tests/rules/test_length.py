import pytest
from rules_engine import Field, Rule
from rules_engine.rules.length import LengthComparisonRule


@pytest.fixture
def sample_data():
    return {
        "tags": ["developer", "python", " Ethiopia"],
        "name": "Abel",
        "profile": {
            "email": "abel@example.com",
            "hobbies": ["reading", "coding"],
            "empty_list": [],
            "none_field": None,
        },
        "age": 30,
        "bio": "Hello world",
        "single_item": [42],
        "empty_string": "",
    }


# ====================== Basic Functionality ======================

def test_length_gt(sample_data):
    rule = Field("tags").len() > 1
    assert rule.evaluate(sample_data) is True


def test_length_eq(sample_data):
    rule = Field("tags").len() == 3
    assert rule.evaluate(sample_data) is True


def test_length_lt(sample_data):
    rule = Field("tags").len() < 5
    assert rule.evaluate(sample_data) is True


def test_length_ge(sample_data):
    rule = Field("tags").len() >= 3
    assert rule.evaluate(sample_data) is True


def test_length_le(sample_data):
    rule = Field("tags").len() <= 3
    assert rule.evaluate(sample_data) is True


def test_length_ne(sample_data):
    rule = Field("tags").len() != 5
    assert rule.evaluate(sample_data) is True


# ====================== Edge Cases ======================

def test_length_none_value(sample_data):
    """None should return False for all operators."""
    rule = Field("profile.none_field").len() > 0
    assert rule.evaluate(sample_data) is False

    rule2 = Field("profile.none_field").len() == 0
    assert rule2.evaluate(sample_data) is False


def test_length_missing_field(sample_data):
    """Missing field (get_nested returns None) should return False."""
    rule = Field("non.existent.field").len() >= 1
    assert rule.evaluate(sample_data) is False


def test_length_empty_list(sample_data):
    rule = Field("profile.empty_list").len() == 0
    assert rule.evaluate(sample_data) is True

    rule2 = Field("profile.empty_list").len() > 0
    assert rule2.evaluate(sample_data) is False


def test_length_empty_string(sample_data):
    rule = Field("empty_string").len() == 0
    assert rule.evaluate(sample_data) is True


def test_length_single_item(sample_data):
    rule = Field("single_item").len() == 1
    assert rule.evaluate(sample_data) is True


def test_length_string(sample_data):
    rule = Field("bio").len() > 5
    assert rule.evaluate(sample_data) is True

    rule2 = Field("name").len() == 4
    assert rule2.evaluate(sample_data) is True


# ====================== Invalid Types ======================

def test_length_invalid_type_int(sample_data):
    rule = Field("age").len() > 1
    assert rule.evaluate(sample_data) is False   # int has no len()


def test_length_invalid_type_none(sample_data):
    rule = Field("profile.none_field").len() == 0
    assert rule.evaluate(sample_data) is False


def test_length_invalid_type_bool(sample_data):
    rule = Field("active").len() >= 1   # if "active" key missing or bool
    data = {"active": True}
    assert rule.evaluate(data) is False


# ====================== Unsupported Operator ======================

def test_length_unsupported_operator(sample_data):
    """Unknown operator should return False."""
    # Create rule directly to bypass Field DSL which only supports valid operators
    rule = LengthComparisonRule(field_name="tags", operator="invalid_op", length=5)
    assert rule.evaluate(sample_data) is False


# ====================== Serialization ======================

def test_length_serialization_roundtrip(sample_data):
    original = Field("tags").len() >= 3

    d = original.to_dict()
    assert d["type"] == "LengthComparisonRule"
    assert d["field"] == "tags"
    assert d["op"] == ">="
    assert d["length"] == 3

    loaded = Rule.from_dict(d)
    assert isinstance(loaded, LengthComparisonRule)
    assert loaded == original
    assert loaded.evaluate(sample_data) is True   # same result


def test_length_from_dict(sample_data):
    data = {
        "type": "LengthComparisonRule",
        "field": "profile.hobbies",
        "op": "<=",
        "length": 2,
    }
    rule = Rule.from_dict(data)
    assert rule.evaluate(sample_data) is True


# ====================== Equality & Repr ======================

def test_length_equality():
    r1 = Field("tags").len() == 3
    r2 = Field("tags").len() == 3
    r3 = Field("tags").len() != 3

    assert r1 == r2
    assert r1 != r3
    assert r1 != "not a rule"


def test_length_repr():
    rule = Field("profile.email").len() >= 10
    repr_str = repr(rule)
    assert "Field('profile.email')" in repr_str
    assert "len() >=" in repr_str
    assert "10" in repr_str


# ====================== Parametrized Tests ======================

@pytest.mark.parametrize(
    "field, operator, length, expected",
    [
        ("tags", "==", 3, True),
        ("tags", "!=", 5, True),
        ("tags", ">", 2, True),
        ("tags", ">=", 3, True),
        ("tags", "<", 10, True),
        ("tags", "<=", 3, True),
        ("profile.empty_list", "==", 0, True),
        ("profile.empty_list", ">", 0, False),
        ("bio", "==", 11, True),
        ("age", "==", 5, False),           # invalid type
        ("profile.none_field", "==", 0, False),
        ("missing.field", ">=", 1, False),
    ],
)
def test_length_parametrized(sample_data, field, operator, length, expected):
    rule = LengthComparisonRule(field_name=field, operator=operator, length=length)
    assert rule.evaluate(sample_data) is expected