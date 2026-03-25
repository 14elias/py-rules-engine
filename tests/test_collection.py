from src.rules_engine.field.field import Field

def test_any_rule(sample_data):
    rule = Field("scores").any(lambda x: x > 25)
    assert rule.evaluate(sample_data)


def test_all_rule(sample_data):
    rule = Field("scores").all(lambda x: x > 5)
    assert rule.evaluate(sample_data)


def test_all_empty():
    rule = Field("scores").all(lambda x: x > 5)
    assert not rule.evaluate({"scores": []})