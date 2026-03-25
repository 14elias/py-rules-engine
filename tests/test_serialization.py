from src.rules_engine.field.field import Field
from src.rules_engine.core.base import Rule
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