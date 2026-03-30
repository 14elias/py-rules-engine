from dataclasses import dataclass
from typing import Any

import pytest

from rules_engine import Rule
from rules_engine.core.combinators import AndRule, NotRule, OrRule, ParenRule

# ====================== TEST  (for building rules) ======================

@dataclass(frozen=True)
class DummyRule(Rule):  # Inherit from Rule 
    value: bool
    name: str = "dummy"

    def evaluate(self, data: Any) -> bool:
        return self.value

    def to_dict(self):
        return {"type": "dummy", "value": self.value, "name": self.name}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(value=data["value"], name=data.get("name", "dummy"))

    def __eq__(self, other):
        if not isinstance(other, DummyRule):
            return False
        return self.value == other.value and self.name == other.name

Rule.register("dummy")(DummyRule)


@pytest.fixture
def T():
    """True predicate"""
    return DummyRule(True, "T")


@pytest.fixture
def F():
    """False predicate"""
    return DummyRule(False, "F")


@pytest.fixture
def A():
    """Another True predicate with different identity"""
    return DummyRule(True, "A")


@pytest.fixture
def B():
    """Another False predicate"""
    return DummyRule(False, "B")


# ====================== REGISTRATION TESTS ======================

def test_logical_rules_are_registered():
    assert "AndRule" in Rule._registry
    assert "OrRule" in Rule._registry
    assert "NotRule" in Rule._registry
    assert "ParenRule" in Rule._registry


# ====================== AND RULE TESTS ======================

class TestAndRule:
    def test_and_true_and_true(self, T, A):
        rule = AndRule(T, A)
        assert rule.evaluate(None) is True

    def test_and_true_and_false(self, T, F):
        rule = AndRule(T, F)
        assert rule.evaluate(None) is False

    def test_and_false_and_true(self, F, T):
        rule = AndRule(F, T)
        assert rule.evaluate(None) is False

    def test_and_false_and_false(self, F, B):
        rule = AndRule(F, B)
        assert rule.evaluate(None) is False

    def test_and_short_circuit(self, F):
        """Left False should not evaluate right side"""
        evaluated_right = [False]

        class SideEffectPredicate(DummyRule):
            def __init__(self):
                super().__init__(value=True, name="side_effect")

            def evaluate(self, data):
                evaluated_right[0] = True
                return True

        rule = AndRule(F, SideEffectPredicate())
        assert rule.evaluate(None) is False
        assert evaluated_right[0] is False

    def test_and_to_dict(self, T, F):
        rule = AndRule(T, F)
        data = rule.to_dict()
        assert data["type"] == "AndRule"
        assert "left" in data
        assert "right" in data

    def test_and_from_dict(self, T, F):
        original = AndRule(T, F)
        serialized = original.to_dict()
        reconstructed = Rule.from_dict(serialized)

        assert isinstance(reconstructed, AndRule)
        assert reconstructed == original

    def test_and_equality(self, T, F, A):
        assert AndRule(T, F) == AndRule(T, F)
        assert AndRule(T, F) != AndRule(F, T)
        assert AndRule(T, F) != AndRule(T, A)


# ====================== OR RULE TESTS ======================

class TestOrRule:
    def test_or_true_or_true(self, T, A):
        rule = OrRule(T, A)
        assert rule.evaluate(None) is True

    def test_or_true_or_false(self, T, F):
        rule = OrRule(T, F)
        assert rule.evaluate(None) is True

    def test_or_false_or_true(self, F, T):
        rule = OrRule(F, T)
        assert rule.evaluate(None) is True

    def test_or_false_or_false(self, F, B):
        rule = OrRule(F, B)
        assert rule.evaluate(None) is False

    def test_or_short_circuit(self, T):
        """Left True should not evaluate right side"""
        evaluated_right = False

        class SideEffectPredicate(Rule):
            def evaluate(self, data):
                nonlocal evaluated_right
                evaluated_right = True
                return False
            def to_dict(self):
                return {"type": "dummy", "value": self.value, "name": self.name}

            @classmethod
            def _from_dict_impl(cls, data):
                return cls(value=data["value"], name=data.get("name", "dummy"))


        rule = OrRule(T, SideEffectPredicate())
        assert rule.evaluate(None) is True
        assert evaluated_right is False   # short-circuited

    def test_or_to_dict(self, T, F):
        rule = OrRule(T, F)
        data = rule.to_dict()
        assert data["type"] == "OrRule"
        assert "left" in data
        assert "right" in data

    def test_or_from_dict(self, T, F):
        original = OrRule(T, F)
        reconstructed = Rule.from_dict(original.to_dict())
        assert isinstance(reconstructed, OrRule)
        assert reconstructed == original

    def test_or_equality(self, T, F):
        assert OrRule(T, F) == OrRule(T, F)
        assert OrRule(T, F) != OrRule(F, T)


# ====================== NOT RULE TESTS ======================

class TestNotRule:
    def test_not_true(self, T):
        rule = NotRule(T)
        assert rule.evaluate(None) is False

    def test_not_false(self, F):
        rule = NotRule(F)
        assert rule.evaluate(None) is True

    def test_not_double_negation(self, T):
        rule = NotRule(NotRule(T))
        assert rule.evaluate(None) is True

    def test_not_to_dict(self, T):
        rule = NotRule(T)
        data = rule.to_dict()
        assert data["type"] == "NotRule"
        assert "child" in data

    def test_not_from_dict(self, T):
        original = NotRule(T)
        reconstructed = Rule.from_dict(original.to_dict())
        assert isinstance(reconstructed, NotRule)
        assert reconstructed == original

    def test_not_equality(self, T, F):
        assert NotRule(T) == NotRule(T)
        assert NotRule(T) != NotRule(F)


# ====================== PAREN RULE TESTS ======================

class TestParenRule:
    def test_paren_passthrough(self, T, F):
        rule = ParenRule(T)
        assert rule.evaluate(None) is True

        rule2 = ParenRule(AndRule(T, F))
        assert rule2.evaluate(None) is False

    def test_paren_to_dict(self, T):
        rule = ParenRule(T)
        data = rule.to_dict()
        assert data["type"] == "ParenRule"
        assert "child" in data

    def test_paren_from_dict(self, T):
        original = ParenRule(T)
        reconstructed = Rule.from_dict(original.to_dict())
        assert isinstance(reconstructed, ParenRule)
        assert reconstructed == original

    def test_paren_equality(self, T, F):
        assert ParenRule(T) == ParenRule(T)
        assert ParenRule(T) != ParenRule(F)

    def test_paren_repr(self, T):
        rule = ParenRule(T)
        assert repr(rule) == f"({T!r})"


# ====================== COMPLEX COMBINATION & ROUNDTRIP TESTS ======================

def test_complex_logical_expression(T, F):
    """Test a realistic nested expression: (T AND F) OR (NOT F)"""
    and_rule = AndRule(T, F)           # False
    not_rule = NotRule(F)              # True
    or_rule = OrRule(and_rule, not_rule)

    assert or_rule.evaluate(None) is True

    # Roundtrip serialization
    serialized = or_rule.to_dict()
    reconstructed = Rule.from_dict(serialized)

    assert isinstance(reconstructed, OrRule)
    assert reconstructed == or_rule
    assert reconstructed.evaluate(None) is True


@pytest.mark.parametrize("left,right,expected", [
    (True, True, True),
    (True, False, False),
    (False, True, False),
    (False, False, False),
])
def test_and_parametrized(left, right, expected, T, F):
    left_rule = T if left else F
    right_rule = T if right else F
    rule = AndRule(left_rule, right_rule)
    assert rule.evaluate(None) is expected


@pytest.mark.parametrize("left,right,expected", [
    (True, True, True),
    (True, False, True),
    (False, True, True),
    (False, False, False),
])
def test_or_parametrized(left, right, expected, T, F):
    left_rule = T if left else F
    right_rule = T if right else F
    rule = OrRule(left_rule, right_rule)
    assert rule.evaluate(None) is expected


# ====================== ERROR HANDLING ======================

def test_from_dict_missing_keys(T):
    with pytest.raises(KeyError):
        Rule.from_dict({"type": "AndRule", "left": T.to_dict()})  # missing "right"

    with pytest.raises(KeyError):
        Rule.from_dict({"type": "NotRule"})  # missing "child"


def test_unknown_rule_type():
    with pytest.raises(ValueError, match="Unknown rule type"):
        Rule.from_dict({"type": "NonExistentRule"})


# ====================== DEEP NESTING & RECURSION SAFETY ======================

def test_deeply_nested_rules(T, F):
    """Ensure deep nesting works and roundtrips correctly"""
    rule = T
    for _ in range(20):
        rule = AndRule(rule, NotRule(ParenRule(OrRule(F, T))))

    serialized = rule.to_dict()
    reconstructed = Rule.from_dict(serialized)

    assert reconstructed == rule
    assert reconstructed.evaluate(None) is False   # because of the inner False