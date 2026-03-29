from rules_engine import Field

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