import pytest
import re
from rules_engine.predicates.base import Predicate
# Adjust these imports based on your actual file structure
from rules_engine.predicates.comparisons import Equals, NotEquals, GreaterThan, LessThan
from rules_engine.predicates.string import Regex, StartsWith, EndsWith
from rules_engine.predicates.collection import Contains, In, LengthEquals, LengthGreaterThan, LengthLessThan
from rules_engine import Field

## --- Comparison Predicate Tests ---

def test_equals_predicate():
    pred = Equals(10)
    assert pred.evaluate(10) is True
    assert pred.evaluate(11) is False
    assert pred == Equals(10)
    assert pred != Equals(20)

def test_greater_than_type_safety():
    pred = GreaterThan(10)
    assert pred.evaluate(15) is True
    assert pred.evaluate(5) is False
    # This hits the 'type(value) != type(self.threshold)' branch for coverage
    assert pred.evaluate("15") is False 

## --- String Predicate Tests ---

def test_regex_predicate():
    pred = Regex(r"^\d{3}$") # Exactly 3 digits
    assert pred.evaluate("123") is True
    assert pred.evaluate("1234") is False
    assert pred.evaluate("abc") is False

def test_starts_ends_with():
    start = StartsWith("hello")
    end = EndsWith("world")
    assert start.evaluate("hello there") is True
    assert end.evaluate("big world") is True
    assert start.evaluate("hi") is False

## --- Collection Predicate Tests ---

def test_contains_and_in():
    cont = Contains("apple")
    assert cont.evaluate(["apple", "banana"]) is True
    assert cont.evaluate("apple pie") is True
    
    is_in = In([1, 2, 3])
    assert is_in.evaluate(2) is True
    assert is_in.evaluate(5) is False

## --- Length Predicate Tests ---

def test_length_predicates():
    eq = LengthEquals(3)
    gt = LengthGreaterThan(2)
    lt = LengthLessThan(5)
    
    sample = [1, 2, 3]
    assert eq.evaluate(sample) is True
    assert gt.evaluate(sample) is True
    assert lt.evaluate(sample) is True
    assert eq.evaluate([1, 2]) is False

## --- Base Registry & Serialization Tests ---

def test_predicate_factory_serialization():
    """Tests the from_dict and registry logic in the Base Predicate class."""
    original = GreaterThan(threshold=25)
    data = original.to_dict()
    
    # Ensure it's using the registry correctly
    loaded = Predicate.from_dict(data)
    
    assert isinstance(loaded, GreaterThan)
    assert loaded.threshold == 25
    assert loaded == original

def test_predicate_invalid_data():
    with pytest.raises(ValueError, match="Predicate must have a 'type' field"):
        Predicate.from_dict({"no_type": "here"})
    
    with pytest.raises(ValueError, match="Unknown predicate type"):
        Predicate.from_dict({"type": "non_existent_predicate"})


def test_string_predicate_failures():
    """Hits the 'False' return paths for string predicates."""
    # Regex: non-match
    assert Regex(r"^\d+$").evaluate("abc") is False
    
    # StartsWith/EndsWith: non-match
    assert StartsWith("apple").evaluate("pineapple") is False
    assert EndsWith("pie").evaluate("apple juice") is False

def test_string_rule_edge_cases():
    """Hits logic in rules/strings.py."""
    # Test case-insensitive matches if your engine supports it
    # and testing against non-string types to trigger error handling
    rule = Field("name").matches(r"^[A-Z]+$")
    assert rule.evaluate({"name": 123}) is False  # Hits type check
    assert rule.evaluate({"age": 25}) is False   # Hits missing field check


def test_collection_edge_cases():
    # 'In' with empty options
    assert In([]).evaluate("anything") is False
    
    # 'Contains' with non-iterable (should handle gracefully)
    try:
        assert Contains("item").evaluate(None) is False
    except (TypeError, AttributeError):
        pass # If your code raises, this helps us see where to add a check

def test_length_rules_on_objects():
    # Testing length on a dictionary or string
    rule = Field("tags").len() == 0
    assert rule.evaluate({"tags": []}) is True
    assert rule.evaluate({"tags": [1, 2]}) is False