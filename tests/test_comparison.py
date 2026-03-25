import pytest
from src.rules_engine.field.field import Field

@pytest.mark.parametrize("value,expected", [
    (20, True),
    (30, False),
])
def test_greater_than(sample_data, value, expected):
    rule = Field("age") > value
    assert rule.evaluate(sample_data) is expected


def test_equality(sample_data):
    rule = Field("country") == "US"
    assert rule.evaluate(sample_data)


def test_missing_field():
    rule = Field("missing") == 10
    assert rule.evaluate({}) is False