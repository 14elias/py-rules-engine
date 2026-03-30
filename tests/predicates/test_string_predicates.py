import re

import pytest

from rules_engine.predicates import EndsWith, Regex, StartsWith
from rules_engine.predicates.base import Predicate

# ====================== Fixture for Predicates ======================

@pytest.fixture
def sample_value():
    """Simple fixture with common values to test predicates against."""
    return {
        "name": "Abel",
        "email": "abel@example.com",
        "bio": "Hello world from Ethiopia",
        "empty_str": "",
        "none_value": None,
        "number": 123,
        "boolean": True,
    }


# ====================== Regex Predicate ======================

def test_regex_basic_match(sample_value):
    pred = Regex(r"^Abel$")
    assert pred.evaluate(sample_value["name"]) is True


def test_regex_partial_match(sample_value):
    pred = Regex(r"example\.com")
    assert pred.evaluate(sample_value["email"]) is True


def test_regex_case_sensitive(sample_value):
    pred = Regex(r"abel")                    # lowercase
    assert pred.evaluate(sample_value["name"]) is False   # 'Abel' does not match


def test_regex_with_word_boundary(sample_value):
    pred = Regex(r"\bworld\b")
    assert pred.evaluate(sample_value["bio"]) is True


def test_regex_no_match(sample_value):
    pred = Regex(r"\d{5}")
    assert pred.evaluate(sample_value["bio"]) is False


def test_regex_on_non_string(sample_value):
    """re.match() on non-string should fail gracefully → False"""
    pred = Regex(r".*")
    assert pred.evaluate(sample_value["number"]) is False
    assert pred.evaluate(sample_value["boolean"]) is False
    assert pred.evaluate(sample_value["none_value"]) is False


def test_regex_empty_string(sample_value):
    pred = Regex(r"^$")
    assert pred.evaluate(sample_value["empty_str"]) is True

    pred2 = Regex(r".+")
    assert pred2.evaluate(sample_value["empty_str"]) is False


def test_regex_invalid_pattern():
    """Invalid regex should raise error at creation time."""
    with pytest.raises(re.error):
        Regex("[")


def test_regex_serialization():
    pred = Regex(r"^[A-Za-z]+$")
    d = pred.to_dict()

    assert d["type"] == "regex"
    assert d["pattern"] == r"^[A-Za-z]+$"

    loaded = Predicate.from_dict(d)
    assert isinstance(loaded, Regex)
    assert loaded == pred
    assert loaded.evaluate("Abel") is True


# ====================== StartsWith Predicate ======================

def test_startswith_success(sample_value):
    pred = StartsWith("Ab")
    assert pred.evaluate(sample_value["name"]) is True


def test_startswith_case_sensitive(sample_value):
    pred = StartsWith("abel")          # lowercase
    assert pred.evaluate(sample_value["name"]) is False


def test_startswith_empty_prefix(sample_value):
    pred = StartsWith("")
    assert pred.evaluate(sample_value["name"]) is True
    assert pred.evaluate(sample_value["empty_str"]) is True


def test_startswith_non_string(sample_value):
    pred = StartsWith("12")
    assert pred.evaluate(sample_value["number"]) is False
    assert pred.evaluate(sample_value["none_value"]) is False


def test_startswith_serialization():
    pred = StartsWith("Hello")
    d = pred.to_dict()

    assert d["type"] == "startswith"
    assert d["prefix"] == "Hello"

    loaded = Predicate.from_dict(d)
    assert isinstance(loaded, StartsWith)
    assert loaded == pred
    assert loaded.evaluate("Hello world") is True


# ====================== EndsWith Predicate ======================

def test_endswith_success(sample_value):
    pred = EndsWith("com")
    assert pred.evaluate(sample_value["email"]) is True


def test_endswith_case_sensitive(sample_value):
    pred = EndsWith("Com")             # wrong case
    assert pred.evaluate(sample_value["email"]) is False


def test_endswith_empty_suffix(sample_value):
    pred = EndsWith("")
    assert pred.evaluate(sample_value["name"]) is True
    assert pred.evaluate(sample_value["empty_str"]) is True


def test_endswith_non_string(sample_value):
    pred = EndsWith("3")
    assert pred.evaluate(sample_value["number"]) is False


def test_endswith_serialization():
    pred = EndsWith("Ethiopia")
    d = pred.to_dict()

    assert d["type"] == "endswith"
    assert d["suffix"] == "Ethiopia"

    loaded = Predicate.from_dict(d)
    assert isinstance(loaded, EndsWith)
    assert loaded == pred
    assert loaded.evaluate("Hello world from Ethiopia") is True


# ====================== Equality Tests ======================

def test_predicate_equality():
    p1 = StartsWith("Ab")
    p2 = StartsWith("Ab")
    p3 = StartsWith("Ac")

    assert p1 == p2
    assert p1 != p3
    assert p1 != "not a predicate"


def test_regex_equality():
    p1 = Regex(r"^\w+$")
    p2 = Regex(r"^\w+$")
    p3 = Regex(r"^\d+$")

    assert p1 == p2
    assert p1 != p3


# ====================== Parametrized Tests ======================

@pytest.mark.parametrize(
    "predicate, value, expected",
    [
        (StartsWith("Ab"), "Abel", True),
        (StartsWith("ab"), "Abel", False),
        (EndsWith("com"), "test@example.com", True),
        (EndsWith("COM"), "test@example.com", False),
        (Regex(r"^Abel$"), "Abel", True),
        (Regex(r"example"), "abel@example.com", True),
        (Regex(r"\d+"), "hello", False),
        (StartsWith(""), "", True),
        (EndsWith(""), "", True),
        (Regex(r"^$"), "", True),
        # Non-string values
        (StartsWith("1"), 123, False),
        (EndsWith("3"), 123, False),
        (Regex(r".*"), 123, False),
    ],
)
def test_predicates_parametrized(predicate, value, expected):
    assert predicate.evaluate(value) is expected