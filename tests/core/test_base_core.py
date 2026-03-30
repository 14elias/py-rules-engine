import pytest

from rules_engine import Field, Rule


@pytest.fixture
def sample_data():
    return {
        "age": 25,
        "country": "US",
        "name": "Abel",
        "tags": ["python", "ai"],
        "scores": [10, 20, 30],
        "profile": {
            "email": "test@example.com"
        }
    }




# ====================== REGISTRY & DISCOVERY TESTS ======================

def test_rule_registry_is_not_empty_after_discovery():
    Rule._discover_rules()
    assert len(Rule._registry) > 0
    assert "AndRule" in Rule._registry
    assert "OrRule" in Rule._registry
    assert "NotRule" in Rule._registry
    assert "ParenRule" in Rule._registry


def test_register_decorator_works():
    @Rule.register("test_temp_rule")
    class TempRule(Rule):
        def evaluate(self, data):
            return True
        def to_dict(self):
            return {"type": "test_temp_rule"}
        @classmethod
        def _from_dict_impl(cls, data):
            return cls()

    assert "test_temp_rule" in Rule._registry
    assert Rule._registry["test_temp_rule"] is TempRule

    # Cleanup
    Rule._registry.pop("test_temp_rule", None)



def test_unknown_rule_type_raises_clear_error():
    with pytest.raises(ValueError, match="Unknown rule type: NonExistentRule"):
        Rule.from_dict({"type": "NonExistentRule"})




def test_and_rule(sample_data):
    rule = (Field("age") > 18) & (Field("country") == "US")
    assert rule.evaluate(sample_data)


def test_or_rule(sample_data):
    rule = (Field("age") < 18) | (Field("country") == "US")
    assert rule.evaluate(sample_data)


def test_not_rule(sample_data):
    rule = ~(Field("age") < 18)
    assert rule.evaluate(sample_data)


def test_logical_short_circuit():
    # OR should stop at the first True
    # AND should stop at the first False
    p_true = Field("a") == 1
    p_false = Field("b") == 2
    
    # These trigger 'all()' and 'any()' logic deeper
    assert (p_true | p_false).evaluate({"a": 1}) is True
    assert (p_false & p_true).evaluate({"b": 3}) is False