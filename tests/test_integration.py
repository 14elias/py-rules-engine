from rules_engine import Field

def test_complex_rule():
    rule = (
        ((Field("age") >= 18) & (Field("country") == "US")) |
        (Field("is_verified") == True)
    )

    data = {"age": 17, "country": "ET", "is_verified": True}
    assert rule.evaluate(data)


def test_complex_fail():
    rule = (
        ((Field("age") >= 18) & (Field("country") == "US")) |
        (Field("is_verified") == True)
    )

    data = {"age": 16, "country": "ET", "is_verified": False}
    assert not rule.evaluate(data)