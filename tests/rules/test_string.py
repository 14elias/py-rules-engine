import re

import pytest

from rules_engine import Field, Rule


@pytest.fixture
def sample_data():
    return {
        "name": "Abel",
        "profile": {
            "email": "abel@example.com",
            "bio": "Hello world!",
            "empty_str": "",
            "none_field": None,
        },
        "age": 30,
        "tags": ["developer", "python"],
    }


# ====================== StartsWithRule ======================

def test_startswith_basic(sample_data):
    rule = Field("name").startswith("Ab")
    assert rule.evaluate(sample_data) is True


def test_startswith_case_sensitive(sample_data):
    rule = Field("name").startswith("ab")  # lowercase
    assert rule.evaluate(sample_data) is False


def test_startswith_empty_prefix(sample_data):
    rule = Field("name").startswith("")
    assert rule.evaluate(sample_data) is True


def test_startswith_non_string_value(sample_data):
    rule = Field("age").startswith("3")
    assert rule.evaluate(sample_data) is False

    rule2 = Field("profile.none_field").startswith("x")
    assert rule2.evaluate(sample_data) is False


def test_startswith_missing_field(sample_data):
    rule = Field("missing.field").startswith("Ab")
    assert rule.evaluate(sample_data) is False


def test_startswith_empty_string_field(sample_data):
    rule = Field("profile.empty_str").startswith("anything")
    assert rule.evaluate(sample_data) is False


def test_startswith_serialization(sample_data):
    rule = Field("name").startswith("Ab")
    serialized = rule.to_dict()
    assert serialized["type"] == "StartsWithRule"
    assert serialized["field"] == "name"
    assert serialized["prefix"] == "Ab"

    loaded = Rule.from_dict(serialized)
    assert isinstance(loaded, type(rule))
    assert loaded == rule
    assert loaded.evaluate(sample_data) is True


# ====================== EndsWithRule ======================

def test_endswith_basic(sample_data):
    rule = Field("name").endswith("el")
    assert rule.evaluate(sample_data) is True


def test_endswith_case_sensitive(sample_data):
    rule = Field("name").endswith("EL")
    assert rule.evaluate(sample_data) is False


def test_endswith_empty_suffix(sample_data):
    rule = Field("name").endswith("")
    assert rule.evaluate(sample_data) is True


def test_endswith_non_string(sample_data):
    rule = Field("age").endswith("0")
    assert rule.evaluate(sample_data) is False


def test_endswith_serialization(sample_data):
    rule = Field("profile.email").endswith(".com")
    serialized = rule.to_dict()
    assert serialized["type"] == "EndsWithRule"
    assert serialized["field"] == "profile.email"
    assert serialized["suffix"] == ".com"

    loaded = Rule.from_dict(serialized)
    assert loaded == rule
    assert loaded.evaluate(sample_data) is True


# ====================== RegexMatchRule ======================

def test_regex_basic_match(sample_data):
    rule = Field("profile.email").matches(r".+@example\.com")
    assert rule.evaluate(sample_data) is True


def test_regex_no_match(sample_data):
    rule = Field("name").matches(r"\d+")
    assert rule.evaluate(sample_data) is False


def test_regex_case_sensitive(sample_data):
    rule = Field("name").matches(r"abel")
    assert rule.evaluate(sample_data) is False  # 'Abel' != 'abel'


def test_regex_with_compiled_pattern(sample_data):
    compiled = re.compile(r"world!")
    rule = Field("profile.bio").matches(compiled)
    assert rule.evaluate(sample_data) is True


def test_regex_non_string_value(sample_data):
    rule = Field("age").matches(r"\d+")
    assert rule.evaluate(sample_data) is False


def test_regex_missing_field(sample_data):
    rule = Field("nonexistent").matches(r".*")
    assert rule.evaluate(sample_data) is False


def test_regex_empty_string(sample_data):
    rule = Field("profile.empty_str").matches(r".+")
    assert rule.evaluate(sample_data) is False

    rule2 = Field("profile.empty_str").matches(r"^$")
    assert rule2.evaluate(sample_data) is True


def test_regex_serialization_roundtrip(sample_data):
    """Ensure compiled regex survives to_dict / from_dict / to_json."""
    original_pattern = r"^[A-Za-z]+$"
    rule = Field("name").matches(original_pattern)

    # to_dict
    d = rule.to_dict()
    assert d["type"] == "RegexMatchRule"
    assert d["field"] == "name"
    assert d["pattern"] == original_pattern

    # from_dict
    loaded = Rule.from_dict(d)
    assert isinstance(loaded, type(rule))
    assert loaded.pattern.pattern == original_pattern
    assert loaded.evaluate({"name": "Abel"}) is True
    assert loaded.evaluate({"name": "Abel123"}) is False

    # to_json / from_json
    json_str = rule.to_json()
    loaded_json = Rule.from_json(json_str)
    assert loaded_json.pattern.pattern == original_pattern


def test_regex_invalid_pattern_raises():
    """__post_init__ should compile the pattern (invalid ones raise at creation)."""
    with pytest.raises(re.error):
        Field("name").matches(r"[")


# ====================== Equality & Repr ======================

def test_rules_equality():
    r1 = Field("name").startswith("Ab")
    r2 = Field("name").startswith("Ab")
    r3 = Field("name").startswith("Ac")

    assert r1 == r2
    assert r1 != r3
    assert r1 != "not a rule"


def test_endswith_equality():
    r1 = Field("name").endswith("el")
    r2 = Field("name").endswith("el")
    assert r1 == r2


def test_regex_equality_with_string_and_compiled():
    r1 = Field("name").matches(r"^\w+$")
    r2 = Field("name").matches(re.compile(r"^\w+$"))
    assert r1 == r2


def test_repr():
    sw = Field("user.name").startswith("Hello")
    ew = Field("user.name").endswith("!")
    rx = Field("email").matches(r".+@example.com")

    assert "startswith" in repr(sw).lower()
    assert "endswith" in repr(ew).lower()   
    assert "matches" in repr(rx).lower()


# ====================== Parametrized Edge Cases ======================

@pytest.mark.parametrize(
    "field, value, rule_type, arg, expected",
    [
        ("name", "Abel", "startswith", "Ab", True),
        ("name", "Abel", "startswith", "ab", False),
        ("name", "Abel", "endswith", "el", True),
        ("name", "Abel", "endswith", "EL", False),
        ("profile.email", "abel@example.com", "matches", r".+@example\.com", True),
        ("age", 30, "startswith", "3", False),
        ("profile.none_field", None, "endswith", "x", False),
        ("missing", "anything", "matches", r".*", False),
    ],
)
def test_rules_parametrized(sample_data, field, value, rule_type, arg, expected):
    test_data = sample_data.copy()
    

    if rule_type == "startswith":
        rule = Field(field).startswith(arg)
    elif rule_type == "endswith":
        rule = Field(field).endswith(arg)
    else:
        rule = Field(field).matches(arg)

    assert rule.evaluate(test_data) is expected