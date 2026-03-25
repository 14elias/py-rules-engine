from src.rules_engine.field.field import Field

def test_and_rule(sample_data):
    rule = (Field("age") > 18) & (Field("country") == "US")
    assert rule.evaluate(sample_data)


def test_or_rule(sample_data):
    rule = (Field("age") < 18) | (Field("country") == "US")
    assert rule.evaluate(sample_data)


def test_not_rule(sample_data):
    rule = ~(Field("age") < 18)
    assert rule.evaluate(sample_data)