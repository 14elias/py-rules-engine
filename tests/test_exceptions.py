import pytest
from rules_engine import Field
from rules_engine.core.base import Rule

def test_invalid_rule_type_deserialization():
    with pytest.raises(ValueError, match="Unknown rule type"):
        Rule.from_dict({"type": "GhostRule", "field": "age"})

def test_type_mismatch_behavior():
    # If age is a string in data but compared as an int
    rule = Field("age") > 18
    # Ensure it returns False gracefully rather than raising TypeError
    assert not rule.evaluate({"age": "not_a_number"})

def test_deep_copy_equality():
    rule = (Field("a") == 1) & (Field("b") == 2)
    new_rule = Rule.from_dict(rule.to_dict())
    assert rule == new_rule  # Tests __eq__ and serialization consistency

def test_none_value_handling():
    """Explicit None in data should not crash the evaluator."""
    rule = Field("age") > 18
    assert rule.evaluate({"age": None}) is False



def test_type_mismatch_graceful_fail():
    """Production data often has stringified numbers. Ensure we don't crash."""
    rule = Field("age") > 18
    # Comparing int to str usually raises TypeError in Python
    # Your engine should handle this or return False
    assert rule.evaluate({"age": "25"}) is False 


def test_none_value_handling():
    """Explicit None in data should not crash the evaluator."""
    rule = Field("age") > 18
    assert rule.evaluate({"age": None}) is False


def test_invalid_collection_type():
    """Calling .contains() or .len() on a non-iterable should return False."""
    rule_contains = Field("age").contains("python")
    rule_len = Field("age").len() > 1
    
    data = {"age": 25} # Int has no len() and is not iterable
    assert rule_contains.evaluate(data) is False
    assert rule_len.evaluate(data) is False



def test_deserialization_invalid_type():
    """Ensure we raise a helpful error for unknown rule types in JSON."""
    invalid_data = {"type": "UnknownRule", "field": "test"}
    with pytest.raises(ValueError, match="Unknown rule type"):
        Rule.from_dict(invalid_data)


def test_serialization_consistency():
    """The 'Golden Rule': rule -> dict -> rule -> dict must be identical."""
    original_rule = (Field("user.score") > 50) & (Field("tags").contains("vip"))
    
    dict_v1 = original_rule.to_dict()
    rule_v2 = Rule.from_dict(dict_v1)
    dict_v2 = rule_v2.to_dict()
    
    assert dict_v1 == dict_v2


def test_regex_serialization_integrity():
    """Regex objects can be tricky. Ensure the pattern string survives round-trip."""
    pattern = r"^[a-z]+$"
    rule = Field("name").matches(pattern)
    
    json_str = rule.to_json()
    loaded_rule = Rule.from_json(json_str)
    
    assert loaded_rule.pattern.pattern == pattern
    assert loaded_rule.evaluate({"name": "abel"})
    assert not loaded_rule.evaluate({"name": "Abel123"})



def test_rule_immutability():
    """Rules should be read-only (frozen) to prevent side effects."""
    rule = Field("age") == 20
    with pytest.raises(Exception): # dataclass(frozen=True) raises FrozenInstanceError
        rule.value = 30 



def test_deep_path_missing_middle():
    """Test access when a middle key in a dot-notation path is missing."""
    rule = Field("organization.department.manager.name") == "Abel"
    
    # organization exists, but department is missing
    data = {"organization": {"location": "Addis Ababa"}}
    assert rule.evaluate(data) is False