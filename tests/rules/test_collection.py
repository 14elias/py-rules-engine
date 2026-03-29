import pytest
from rules_engine import Field, Rule
from rules_engine.rules.collection import AnyRule, AllRule
from rules_engine.predicates import Contains, GreaterThan, Equals
# If you have more predicates, you can import them too


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

# ====================== AnyRule Tests ======================

def test_any_rule_success(sample_data):
    """At least one item matches the predicate."""
    rule = Field("tags").any(Contains("ai"))
    assert rule.evaluate(sample_data) is True


def test_any_rule_no_match(sample_data):
    """No item matches the predicate."""
    rule = Field("tags").any(Contains("java"))
    assert rule.evaluate(sample_data) is False


def test_any_rule_with_numbers(sample_data):
    rule = Field("scores").any(GreaterThan(25))
    assert rule.evaluate(sample_data) is True   # 30 > 25


def test_any_rule_all_fail(sample_data):
    rule = Field("scores").any(GreaterThan(100))
    assert rule.evaluate(sample_data) is False


def test_any_rule_empty_collection(sample_data):
    """Empty list/tuple/set should return False for any()."""
    rule = Field("profile.empty_list").any(Contains("x"))
    assert rule.evaluate(sample_data) is False


def test_any_rule_non_collection(sample_data):
    """Non-list/tuple/set should return False."""
    rule = Field("age").any(Equals(25))
    assert rule.evaluate(sample_data) is False

    rule2 = Field("name").any(Contains("A"))
    assert rule2.evaluate(sample_data) is False

    rule3 = Field("profile.none_value").any(GreaterThan(0))
    assert rule3.evaluate(sample_data) is False


def test_any_rule_missing_field(sample_data):
    rule = Field("non.existent").any(Contains("ai"))
    assert rule.evaluate(sample_data) is False


def test_any_rule_with_tuple(sample_data):
    rule = Field("single_tuple").any(Equals(2))
    assert rule.evaluate(sample_data) is True


def test_any_rule_with_set(sample_data):
    data = sample_data.copy()
    data["unique_tags"] = {"python", "ai"}
    rule = Field("unique_tags").any(Contains("ai"))
    assert rule.evaluate(data) is True


# ====================== AllRule Tests ======================

def test_all_rule_success(sample_data):
    """All items match the predicate."""
    rule = Field("scores").all(GreaterThan(5))
    assert rule.evaluate(sample_data) is True


def test_all_rule_partial_match(sample_data):
    """Not all items match → False."""
    rule = Field("scores").all(GreaterThan(15))
    assert rule.evaluate(sample_data) is False   # 10 is not > 15


def test_all_rule_empty_collection(sample_data):
    """Empty collection should return False (as per your implementation)."""
    rule = Field("profile.empty_list").all(GreaterThan(0))
    assert rule.evaluate(sample_data) is False


def test_all_rule_non_collection(sample_data):
    rule = Field("age").all(GreaterThan(10))
    assert rule.evaluate(sample_data) is False


def test_all_rule_missing_field(sample_data):
    rule = Field("missing.field").all(Equals(10))
    assert rule.evaluate(sample_data) is False


def test_all_rule_with_strings(sample_data):
    """All characters in string? But string is not allowed → False"""
    rule = Field("bio").all(Contains("o"))
    assert rule.evaluate(sample_data) is False


def test_all_rule_single_item(sample_data):
    rule = Field("single_tuple").all(Equals(1))   # only first item is 1, others fail
    assert rule.evaluate(sample_data) is False

    rule2 = Field("single_tuple").all(GreaterThan(0))
    assert rule2.evaluate(sample_data) is True


# ====================== Serialization ======================

def test_any_rule_serialization_roundtrip(sample_data):
    original = Field("tags").any(Contains("ai"))

    d = original.to_dict()
    assert d["type"] == "AnyRule"
    assert d["field"] == "tags"
    assert d["predicate"]["type"] == "contains"   # assuming Contains has type

    loaded = Rule.from_dict(d)
    assert isinstance(loaded, AnyRule)
    assert loaded == original
    assert loaded.evaluate(sample_data) is True


def test_all_rule_serialization_roundtrip(sample_data):
    original = Field("scores").all(GreaterThan(5))

    loaded = Rule.from_dict(original.to_dict())
    assert isinstance(loaded, AllRule)
    assert loaded == original
    assert loaded.evaluate(sample_data) is True


# ====================== Equality ======================

def test_any_rule_equality():
    p1 = Contains("ai")
    p2 = Contains("ai")
    r1 = Field("tags").any(p1)
    r2 = Field("tags").any(p2)
    r3 = Field("tags").any(Contains("java"))

    assert r1 == r2
    assert r1 != r3


def test_all_rule_equality():
    r1 = Field("scores").all(GreaterThan(5))
    r2 = Field("scores").all(GreaterThan(5))
    assert r1 == r2


# ====================== Parametrized Tests ======================

@pytest.mark.parametrize(
    "rule_builder, expected",
    [
        (lambda: Field("tags").any(Contains("ai")), True),
        (lambda: Field("tags").any(Contains("java")), False),
        (lambda: Field("scores").any(GreaterThan(25)), True),
        (lambda: Field("scores").any(GreaterThan(100)), False),
        (lambda: Field("profile.empty_list").any(Contains("x")), False),
        (lambda: Field("age").any(Equals(25)), False),
        (lambda: Field("scores").all(GreaterThan(5)), True),
        (lambda: Field("scores").all(GreaterThan(15)), False),
        (lambda: Field("profile.empty_list").all(GreaterThan(0)), False),
        (lambda: Field("single_tuple").all(GreaterThan(0)), True),
    ],
)
def test_any_all_parametrized(sample_data, rule_builder, expected):
    rule = rule_builder()
    assert rule.evaluate(sample_data) is expected