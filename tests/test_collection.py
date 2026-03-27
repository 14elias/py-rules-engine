from src.rules_engine.field.field import Field
from src.rules_engine.predicates.collection import Contains
from src.rules_engine.predicates.comparisons import GreaterThan


def test_any_rule(sample_data):
    rule = Field("tags").any(Contains("ai"))
    assert rule.evaluate(sample_data)


def test_all_rule(sample_data):
    rule = Field("scores").all(GreaterThan(5))
    assert rule.evaluate(sample_data)


def test_all_empty():
    rule = Field("scores").all(GreaterThan(5))
    assert not rule.evaluate({"scores": []})