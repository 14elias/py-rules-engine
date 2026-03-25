from src.rules_engine.field.field import Field

def test_startswith(sample_data):
    rule = Field("name").startswith("Ab")
    assert rule.evaluate(sample_data)


def test_regex_match(sample_data):
    rule = Field("profile.email").matches(r".+@example\.com")
    assert rule.evaluate(sample_data)


def test_regex_fail(sample_data):
    rule = Field("name").matches(r"\d+")
    assert not rule.evaluate(sample_data)