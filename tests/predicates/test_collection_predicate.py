
import pytest
from rules_engine.predicates.base import Predicate
from rules_engine.predicates import Contains, In, LengthEquals, LengthGreaterThan, LengthLessThan


# ====================== HELPER FIXTURES ======================

@pytest.fixture
def sample_data():
    """Common test data for different types"""
    return {
        "string": "hello world",
        "list": [1, 2, 3, 4, 5],
        "tuple": (10, 20, 30),
        "set": {1, 2, 3},
        "dict": {"a": 1, "b": 2},
        "empty_list": [],
        "empty_string": "",
    }


# ====================== BASE SERIALIZATION TESTS ======================

def test_predicate_registration():
    """Ensure all predicates are properly registered"""
    assert "contains" in Predicate._registry
    assert "in" in Predicate._registry
    assert "len_eq" in Predicate._registry
    assert "len_gt" in Predicate._registry
    assert "len_lt" in Predicate._registry


# ====================== CONTAINS PREDICATE TESTS ======================

class TestContains:
    def test_contains_string(self, sample_data):
        pred = Contains("world")
        assert pred.evaluate(sample_data["string"]) is True
        assert pred.evaluate("python world") is True
        assert pred.evaluate("hello") is False

    def test_contains_list(self, sample_data):
        pred = Contains(3)
        assert pred.evaluate(sample_data["list"]) is True
        assert pred.evaluate([1, 2, 4]) is False

    def test_contains_tuple(self, sample_data):
        pred = Contains(20)
        assert pred.evaluate(sample_data["tuple"]) is True

    def test_contains_set(self, sample_data):
        pred = Contains(2)
        assert pred.evaluate(sample_data["set"]) is True

    def test_contains_not_iterable(self):
        pred = Contains("x")
        with pytest.raises(TypeError):
            pred.evaluate(123)          # int is not iterable
        with pytest.raises(TypeError):
            pred.evaluate(None)

    def test_contains_to_dict(self):
        pred = Contains("test_item")
        data = pred.to_dict()
        assert data == {"type": "contains", "item": "test_item"}

    def test_contains_from_dict(self):
        data = {"type": "contains", "item": 42}
        pred = Predicate.from_dict(data)
        assert isinstance(pred, Contains)
        assert pred.item == 42
        assert pred.evaluate([1, 2, 42, 3]) is True

    def test_contains_equality(self):
        pred1 = Contains("hello")
        pred2 = Contains("hello")
        pred3 = Contains("world")

        assert pred1 == pred2
        assert pred1 != pred3
        assert pred1 != "not a predicate"


# ====================== IN PREDICATE TESTS ======================

class TestIn:
    def test_in_list(self, sample_data):
        pred = In([1, 2, 3, 4, 5])
        assert pred.evaluate(3) is True
        assert pred.evaluate(10) is False

    def test_in_tuple(self):
        pred = In((10, 20, 30))
        assert pred.evaluate(20) is True
        assert pred.evaluate(99) is False

    def test_in_set(self):
        pred = In({1, 2, 3})
        assert pred.evaluate(2) is True

    def test_in_string(self):
        pred = In("abcde")
        assert pred.evaluate("c") is True
        assert pred.evaluate("z") is False

    def test_in_to_dict(self):
        options = [1, 2, 3]
        pred = In(options)
        data = pred.to_dict()
        assert data == {"type": "in", "options": [1, 2, 3]}

    def test_in_from_dict(self):
        data = {"type": "in", "options": ["red", "green", "blue"]}
        pred = Predicate.from_dict(data)
        assert isinstance(pred, In)
        assert pred.options == ["red", "green", "blue"]
        assert pred.evaluate("green") is True

    def test_in_equality(self):
        pred1 = In([1, 2, 3])
        pred2 = In([1, 2, 3])
        pred3 = In([4, 5, 6])

        assert pred1 == pred2
        assert pred1 != pred3


# ====================== LENGTH PREDICATES TESTS ======================

class TestLengthEquals:
    def test_len_eq_list(self, sample_data):
        pred = LengthEquals(5)
        assert pred.evaluate(sample_data["list"]) is True
        assert pred.evaluate([1, 2, 3]) is False

    def test_len_eq_string(self, sample_data):
        pred = LengthEquals(11)
        assert pred.evaluate(sample_data["string"]) is True  # "hello world"

    def test_len_eq_empty(self, sample_data):
        pred = LengthEquals(0)
        assert pred.evaluate(sample_data["empty_list"]) is True
        assert pred.evaluate(sample_data["empty_string"]) is True

    def test_len_eq_to_dict(self):
        pred = LengthEquals(42)
        assert pred.to_dict() == {"type": "len_eq", "length": 42}

    def test_len_eq_from_dict(self):
        pred = Predicate.from_dict({"type": "len_eq", "length": 10})
        assert isinstance(pred, LengthEquals)
        assert pred.length == 10
        assert pred.evaluate("abcdefghij") is True

    def test_len_eq_equality(self):
        assert LengthEquals(5) == LengthEquals(5)
        assert LengthEquals(5) != LengthEquals(10)


class TestLengthGreaterThan:
    def test_len_gt(self, sample_data):
        pred = LengthGreaterThan(3)
        assert pred.evaluate(sample_data["list"]) is True      # len=5
        assert pred.evaluate([1, 2]) is False

    def test_len_gt_string(self, sample_data):
        pred = LengthGreaterThan(10)
        assert pred.evaluate(sample_data["string"]) is True

    def test_len_gt_to_dict(self):
        assert LengthGreaterThan(7).to_dict() == {"type": "len_gt", "length": 7}

    def test_len_gt_from_dict(self):
        pred = Predicate.from_dict({"type": "len_gt", "length": 4})
        assert pred.evaluate([1, 2, 3, 4, 5]) is True

    def test_len_gt_equality(self):
        assert LengthGreaterThan(5) == LengthGreaterThan(5)
        assert LengthGreaterThan(5) != LengthGreaterThan(6)


class TestLengthLessThan:
    def test_len_lt(self, sample_data):
        pred = LengthLessThan(10)
        assert pred.evaluate(sample_data["list"]) is True      # 5 < 10
        assert pred.evaluate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) is False

    def test_len_lt_empty(self, sample_data):
        pred = LengthLessThan(1)
        assert pred.evaluate(sample_data["empty_list"]) is True

    def test_len_lt_to_dict(self):
        assert LengthLessThan(3).to_dict() == {"type": "len_lt", "length": 3}

    def test_len_lt_from_dict(self):
        pred = Predicate.from_dict({"type": "len_lt", "length": 2})
        assert pred.evaluate([1]) is True
        assert pred.evaluate([1, 2, 3]) is False

    def test_len_lt_equality(self):
        assert LengthLessThan(8) == LengthLessThan(8)
        assert LengthLessThan(8) != LengthLessThan(7)


# ====================== EDGE CASES & ERROR HANDLING ======================

def test_length_predicates_with_non_sized_objects():
    """Test behavior when value has no __len__"""
    for Pred in (LengthEquals, LengthGreaterThan, LengthLessThan):
        pred = Pred(5)
        with pytest.raises(TypeError):
            pred.evaluate(123)           # int has no len()
        with pytest.raises(TypeError):
            pred.evaluate(None)
        with pytest.raises(TypeError):
            pred.evaluate(3.14)


def test_serialization_roundtrip():
    """Test full serialization + deserialization roundtrip for all predicates"""
    test_cases = [
        Contains("secret"),
        In([1, 2, 3, "admin"]),
        LengthEquals(0),
        LengthGreaterThan(10),
        LengthLessThan(5),
    ]

    for original in test_cases:
        data = original.to_dict()
        reconstructed = Predicate.from_dict(data)
        
        assert isinstance(reconstructed, original.__class__)
        assert reconstructed == original
        # Also test that evaluate still works the same
        assert reconstructed.evaluate([1, 2, 3, 4, 5]) == original.evaluate([1, 2, 3, 4, 5])


def test_invalid_from_dict():
    """Test graceful handling of malformed dicts"""
    with pytest.raises(KeyError):
        Predicate.from_dict({"type": "contains"})  # missing "item"

    with pytest.raises(KeyError):
        Predicate.from_dict({"type": "in"})        # missing "options"

    with pytest.raises(KeyError):
        Predicate.from_dict({"type": "len_eq"})    # missing "length"


def test_unknown_predicate_type():
    """Test that unknown predicate types raise appropriate error"""
    with pytest.raises(ValueError, match="Unknown predicate type"):
        Predicate.from_dict({"type": "non_existent"})