import pytest
from rules_engine.predicates.logical import And, Or, Not
from rules_engine.predicates.comparisons import GreaterThan, Equals

def test_and_predicate():
    # age > 20 AND age == 25
    p1 = GreaterThan(20)
    p2 = Equals(25)
    logic = And(p1, p2)
    
    assert logic.evaluate(25) is True
    assert logic.evaluate(19) is False
    assert logic.evaluate(21) is False # Greater than 20 but not 25

def test_or_predicate():
    # age > 30 OR age == 25
    p1 = GreaterThan(30)
    p2 = Equals(25)
    logic = Or(p1, p2)
    
    assert logic.evaluate(31) is True
    assert logic.evaluate(25) is True
    assert logic.evaluate(20) is False

def test_not_predicate():
    # NOT (age == 25)
    p1 = Equals(25)
    logic = Not(p1)
    
    assert logic.evaluate(30) is True
    assert logic.evaluate(25) is False

def test_logical_equality():
    # Test __eq__ for And
    and1 = And(Equals(1), Equals(2))
    and2 = And(Equals(1), Equals(2))
    and3 = And(Equals(1))
    
    assert and1 == and2
    assert and1 != and3
    assert and1 != "not a predicate"

    # Test __eq__ for Not
    not1 = Not(Equals(1))
    not2 = Not(Equals(1))
    assert not1 == not2

def test_logical_serialization_roundtrip():
    # Complex nested: (age > 20 AND age < 30)
    original = And(GreaterThan(20), Equals(25))
    
    data = original.to_dict()
    # This triggers the _from_dict_impl you wrote
    from rules_engine.predicates.base import Predicate
    loaded = Predicate.from_dict(data)
    
    assert original == loaded
    assert isinstance(loaded, And)