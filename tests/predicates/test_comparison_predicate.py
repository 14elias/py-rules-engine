import pytest

from rules_engine.predicates import (
    Equals,
    GreaterThan,
    GreaterThanOrEqual,
    LessThan,
    LessThanOrEqual,
    NotEquals,
)
from rules_engine.predicates.base import Predicate

# ====================== Fixtures ======================


@pytest.fixture
def sample_value():
    """Common test values with different types."""
    return {
        "name": "Abel",
        "age": 28,
        "score": 85.5,
        "active": True,
        "tags": ["developer", "ethiopia"],
        "none_value": None,
        "empty_str": "",
        "zero": 0,
        "false_bool": False,
        "pi": 3.14159,
    }


# ====================== Equals Predicate ======================


class TestEquals:
    def test_equals_basic(self, sample_value):
        pred = Equals("Abel")
        assert pred.evaluate(sample_value["name"]) is True

    def test_equals_with_number(self, sample_value):
        pred = Equals(28)
        assert pred.evaluate(sample_value["age"]) is True

    def test_equals_with_float(self, sample_value):
        pred = Equals(85.5)
        assert pred.evaluate(sample_value["score"]) is True

    def test_equals_with_boolean(self, sample_value):
        pred = Equals(True)
        assert pred.evaluate(sample_value["active"]) is True

    def test_equals_fails_different_value(self, sample_value):
        pred = Equals("John")
        assert pred.evaluate(sample_value["name"]) is False

    def test_equals_type_sensitive(self, sample_value):
        """28 != '28'"""
        pred = Equals(28)
        assert pred.evaluate("28") is False
        assert pred.evaluate(28.0) is False  # int != float

    def test_equals_none(self, sample_value):
        pred = Equals(None)
        assert pred.evaluate(sample_value["none_value"]) is True
        assert pred.evaluate("None") is False

    @pytest.mark.parametrize(
        "value, expected",
        [
            ("", True),
            (0, True),
            (False, True),
            (None, True),
        ],
    )
    def test_equals_edge_values(self, sample_value, value, expected):
        pred = Equals(value)

        key = ""
        if value is None:
            key = "none_value"
        elif value is False:
            key = "false_bool"
        elif value == 0:
            key = "zero"
        else:
            key = "empty_str"
        assert pred.evaluate(sample_value[key]) is expected


# ====================== NotEquals Predicate ======================


class TestNotEquals:
    def test_not_equals_basic(self, sample_value):
        pred = NotEquals("John")
        assert pred.evaluate(sample_value["name"]) is True

    def test_not_equals_same_value(self, sample_value):
        pred = NotEquals("Abel")
        assert pred.evaluate(sample_value["name"]) is False

    def test_not_equals_type_sensitive(self, sample_value):
        pred = NotEquals(28)
        assert pred.evaluate(28) is False
        assert pred.evaluate("28") is True
        assert pred.evaluate(28.0) is True


# ====================== GreaterThan / GreaterThanOrEqual ======================


class TestGreaterThan:
    def test_gt_success(self, sample_value):
        pred = GreaterThan(25)
        assert pred.evaluate(sample_value["age"]) is True

    def test_gt_failure(self, sample_value):
        pred = GreaterThan(30)
        assert pred.evaluate(sample_value["age"]) is False

    def test_gt_type_mismatch(self, sample_value):
        pred = GreaterThan(25)
        assert pred.evaluate("30") is False  # str vs int
        assert pred.evaluate(25.0) is False  # float vs int

    def test_gt_with_floats(self, sample_value):
        pred = GreaterThan(3.14)
        assert pred.evaluate(sample_value["pi"]) is True


class TestGreaterThanOrEqual:
    def test_gte_success_equal(self, sample_value):
        pred = GreaterThanOrEqual(28)
        assert pred.evaluate(sample_value["age"]) is True

    def test_gte_success_greater(self, sample_value):
        pred = GreaterThanOrEqual(20)
        assert pred.evaluate(sample_value["age"]) is True

    def test_gte_type_mismatch(self, sample_value):
        pred = GreaterThanOrEqual(85)
        assert pred.evaluate(85.5) is False  # int vs float


# ====================== LessThan / LessThanOrEqual ======================


class TestLessThan:
    def test_lt_success(self, sample_value):
        pred = LessThan(30)
        assert pred.evaluate(sample_value["age"]) is True

    def test_lt_failure(self, sample_value):
        pred = LessThan(20)
        assert pred.evaluate(sample_value["age"]) is False

    def test_lt_type_mismatch(self, sample_value):
        pred = LessThan(100)
        assert pred.evaluate("50") is False


class TestLessThanOrEqual:
    def test_lte_success_equal(self, sample_value):
        pred = LessThanOrEqual(28)
        assert pred.evaluate(sample_value["age"]) is True

    def test_lte_success_less(self, sample_value):
        pred = LessThanOrEqual(30)
        assert pred.evaluate(sample_value["age"]) is True


# ====================== Parametrized Comprehensive Tests ======================


@pytest.mark.parametrize(
    "predicate_cls, threshold, test_value, expected",
    [
        # Equals
        (Equals, 28, 28, True),
        (Equals, 28, 29, False),
        (Equals, "Abel", "Abel", True),
        (Equals, "Abel", "abel", False),  # case sensitive
        (Equals, True, True, True),
        (Equals, None, None, True),
        # NotEquals
        (NotEquals, 28, 29, True),
        (NotEquals, 28, 28, False),
        # GreaterThan
        (GreaterThan, 25, 28, True),
        (GreaterThan, 28, 28, False),
        (GreaterThan, 30, 28, False),
        # GreaterThanOrEqual
        (GreaterThanOrEqual, 28, 28, True),
        (GreaterThanOrEqual, 25, 28, True),
        (GreaterThanOrEqual, 30, 28, False),
        # LessThan
        (LessThan, 30, 28, True),
        (LessThan, 28, 28, False),
        # LessThanOrEqual
        (LessThanOrEqual, 28, 28, True),
        (LessThanOrEqual, 30, 28, True),
        (LessThanOrEqual, 25, 28, False),
    ],
)
def test_comparison_predicates_param(predicate_cls, threshold, test_value, expected):
    pred = predicate_cls(threshold)
    assert pred.evaluate(test_value) is expected


# ====================== Serialization Tests ======================


@pytest.mark.parametrize(
    "predicate_cls, value",
    [
        (Equals, "Abel"),
        (Equals, 100),
        (NotEquals, 0),
        (GreaterThan, 18),
        (GreaterThanOrEqual, 85.5),
        (LessThan, 100),
        (LessThanOrEqual, 25),
    ],
)
def test_serialization_roundtrip(predicate_cls, value):
    original = predicate_cls(value)
    data = original.to_dict()

    assert data["type"] == original._type
    assert data.get("expected") == value or data.get("threshold") == value

    loaded = Predicate.from_dict(data)
    assert isinstance(loaded, predicate_cls)
    assert loaded == original


# ====================== Equality Tests ======================


def test_equality():
    assert Equals(28) == Equals(28)
    assert Equals(28) != Equals(29)
    assert NotEquals(10) == NotEquals(10)
    assert GreaterThan(5) == GreaterThan(5)
    assert GreaterThan(5) != GreaterThan(6)
    assert GreaterThanOrEqual(10) == GreaterThanOrEqual(10)
    assert LessThan(100) != LessThanOrEqual(100)


def test_equality_across_different_classes():
    eq = Equals(28)
    gt = GreaterThan(28)
    assert eq != gt


# ====================== Edge Cases ======================


def test_with_none_values():
    assert Equals(None).evaluate(None) is True
    assert NotEquals(None).evaluate(None) is False
    assert GreaterThan(0).evaluate(None) is False
    assert LessThan(100).evaluate(None) is False


def test_comparison_with_different_types():
    """All numeric comparisons should be strict about type."""
    assert GreaterThan(10).evaluate(10.0) is False
    assert GreaterThanOrEqual(5).evaluate("5") is False
    assert LessThan(100).evaluate(True) is False


def test_empty_string_handling():
    assert Equals("").evaluate("") is True
    assert NotEquals("").evaluate("") is False
    assert GreaterThan("").evaluate("a") is True
