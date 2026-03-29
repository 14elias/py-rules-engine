from rules_engine import Field
from rules_engine.core.base import Rule

def test_round_trip_dict(sample_data):
    rule = (Field("age") > 18) & (Field("country") == "US")

    data = rule.to_dict()
    loaded = Rule.from_dict(data)

    assert loaded.evaluate(sample_data)


def test_round_trip_json(sample_data):
    rule = (Field("age") > 18) | (Field("country") == "ET")

    json_str = rule.to_json()
    loaded = Rule.from_json(json_str)

    assert loaded.evaluate(sample_data)


def test_serialization_consistency():
    """The 'Golden Rule': rule -> dict -> rule -> dict must be identical."""
    original_rule = (Field("user.score") > 50) & (Field("tags").contains("vip"))
    
    dict_v1 = original_rule.to_dict()
    rule_v2 = Rule.from_dict(dict_v1)
    dict_v2 = rule_v2.to_dict()
    
    assert dict_v1 == dict_v2