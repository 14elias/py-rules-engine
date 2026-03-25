from src.rules_engine.field.field import Field

def test_length_gt(sample_data):
    rule = Field("tags").len() > 1
    assert rule.evaluate(sample_data)


def test_length_eq(sample_data):
    rule = Field("tags").len() == 2
    assert rule.evaluate(sample_data)


def test_length_invalid_type():
    rule = Field("age").len() > 1
    assert not rule.evaluate({"age": 10})