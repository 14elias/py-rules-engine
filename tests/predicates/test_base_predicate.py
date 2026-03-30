import pytest

from rules_engine.predicates.base import Predicate
from rules_engine.predicates.comparisons import GreaterThan


def test_predicate_factory_serialization():
    """Tests the from_dict and registry logic in the Base Predicate class."""
    original = GreaterThan(threshold=25)
    data = original.to_dict()
    
    loaded = Predicate.from_dict(data)
    
    assert isinstance(loaded, GreaterThan)
    assert loaded.threshold == 25
    assert loaded == original


def test_predicate_invalid_data():
    with pytest.raises(ValueError, match="Predicate must have a 'type' field"):
        Predicate.from_dict({"no_type": "here"})
    
    with pytest.raises(ValueError, match="Unknown predicate type"):
        Predicate.from_dict({"type": "non_existent_predicate"})

