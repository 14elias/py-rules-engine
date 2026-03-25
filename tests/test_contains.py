from src.rules_engine.field.field import Field

def test_contains_success(sample_data):
    rule = Field("tags").contains("python")
    assert rule.evaluate(sample_data)


def test_contains_fail(sample_data):
    rule = Field("tags").contains("java")
    assert not rule.evaluate(sample_data)