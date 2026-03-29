import pytest
from rules_engine.predicates import Regex, StartsWith, EndsWith, And, Or, Not
from rules_engine.predicates.base import Predicate
from rules_engine.predicates.comparisons import GreaterThan, Equals


# ====================== Fixtures ======================

@pytest.fixture
def sample_value():
    """Common test data used across logical predicate tests."""
    return {
        "name": "Abel",
        "email": "abel@example.com",
        "bio": "Hello world from Ethiopia",
        "empty_str": "",
        "none_value": None,
        "number": 123,
        "boolean": True,
        "city": "Addis Ababa",
    }


@pytest.fixture
def simple_predicates(sample_value):
    """Reusable basic predicates for composition."""
    return {
        "starts_abel": StartsWith("Abel"),
        "starts_ab": StartsWith("Ab"),
        "ends_com": EndsWith("com"),
        "regex_abel": Regex(r"^Abel$"),
        "regex_ethiopia": Regex(r"Ethiopia"),
        "always_true": Regex(r".*"),      # matches any string
        "always_false": Regex(r"^$"),     # only matches empty string
    }


# ====================== And Predicate Tests ======================

def test_and_empty():
    """And with no predicates should return True (vacuous truth)."""
    pred = And()
    assert pred.evaluate("anything") is True
    assert pred.evaluate(123) is True
    assert pred.evaluate(None) is True


def test_and_single_predicate(sample_value, simple_predicates):
    """And with one predicate should behave exactly like that predicate."""
    p = simple_predicates["starts_ab"]
    and_pred = And(p)

    assert and_pred.evaluate(sample_value["name"]) is True
    assert and_pred.evaluate("xyz") is False


def test_and_multiple_all_true(sample_value, simple_predicates):
    pred = And(
        simple_predicates["starts_ab"],
        simple_predicates["ends_com"],
        simple_predicates["regex_ethiopia"]
    )
    assert pred.evaluate(sample_value["bio"]) is False   # bio doesn't end with "com"
    assert pred.evaluate(sample_value["email"]) is False # email doesn't contain "Ethiopia"


def test_and_short_circuit(sample_value, simple_predicates):
    """And should stop evaluating once it finds a False predicate."""
    call_count = [0]  # mutable to modify inside inner class

    class CountingFalsePredicate(Predicate):
        """A real Predicate that counts how many times it's evaluated."""
        def evaluate(self, value):
            call_count[0] += 1
            return False

        def to_dict(self):
            return {"type": "counting_false", "value": False}

        @classmethod
        def _from_dict_impl(cls, data):
            return cls()

    false_pred = CountingFalsePredicate()

    and_pred = And(
        simple_predicates["starts_ab"],   # True for "Abel"
        false_pred,                       # False → should short-circuit
        simple_predicates["always_true"]  # This should NOT be evaluated
    )

    result = and_pred.evaluate(sample_value["name"])
    assert result is False
    assert call_count[0] == 1   # Only the second predicate was called


@pytest.mark.parametrize(
    "predicates, value, expected",
    [
        # All true
        ([StartsWith("Ab"), EndsWith("el")], "Abel", True),
        # One false
        ([StartsWith("Ab"), EndsWith("xyz")], "Abel", False),
        # All false
        ([StartsWith("xy"), EndsWith("zz")], "Abel", False),
        # With non-string value
        ([StartsWith("Ab"), Regex(r".*")], 123, False),
        ([StartsWith(""), Regex(r"^$")], "", True),
    ],
)
def test_and_parametrized(predicates, value, expected):
    and_pred = And(*predicates)
    assert and_pred.evaluate(value) is expected


# ====================== Or Predicate Tests ======================

def test_or_empty():
    """Or with no predicates should return False (vacuous falsity)."""
    pred = Or()
    assert pred.evaluate("anything") is False
    assert pred.evaluate(None) is False


def test_or_single_predicate(sample_value, simple_predicates):
    p = simple_predicates["regex_abel"]
    or_pred = Or(p)
    assert or_pred.evaluate(sample_value["name"]) is True
    assert or_pred.evaluate("xyz") is False


def test_or_short_circuit(sample_value, simple_predicates):
    """Or should stop evaluating once it finds a True predicate."""
    call_count = [0]

    class CountingTruePredicate(Predicate):
        """A real Predicate that counts how many times it's evaluated."""
        def evaluate(self, value):
            call_count[0] += 1
            return True

        def to_dict(self):
            return {"type": "counting_true", "value": True}

        @classmethod
        def _from_dict_impl(cls, data):
            return cls()

    true_pred = CountingTruePredicate()

    or_pred = Or(
        simple_predicates["always_false"],  # False
        true_pred,                          # True → should short-circuit
        simple_predicates["always_false"]   # This should NOT be evaluated
    )

    result = or_pred.evaluate(sample_value["name"])
    assert result is True
    assert call_count[0] == 1   # Only the second predicate was called


@pytest.mark.parametrize(
    "predicates, value, expected",
    [
        ([StartsWith("Ab"), EndsWith("com")], "Abel", True),      # first is True
        ([StartsWith("xy"), EndsWith("el")], "Abel", True),       # second is True
        ([StartsWith("xy"), EndsWith("zz")], "Abel", False),      # both False
        ([Regex(r"\d+"), Regex(r"Abel")], "Abel", True),
        ([StartsWith(""), EndsWith("")], "", True),
        # Non-string
        ([StartsWith("1"), EndsWith("3")], 123, False),
    ],
)
def test_or_parametrized(predicates, value, expected):
    or_pred = Or(*predicates)
    assert or_pred.evaluate(value) is expected


# ====================== Not Predicate Tests ======================

def test_not_basic(sample_value, simple_predicates):
    pred = Not(simple_predicates["starts_ab"])
    assert pred.evaluate(sample_value["name"]) is False   # "Abel" starts with "Ab" → Not = False
    assert pred.evaluate("xyz") is True


def test_not_double_negation(sample_value, simple_predicates):
    """Not(Not(p)) should equal p."""
    p = simple_predicates["regex_abel"]
    double_not = Not(Not(p))
    assert double_not.evaluate(sample_value["name"]) is True
    assert double_not.evaluate("xyz") is False


@pytest.mark.parametrize(
    "inner_predicate, value, expected",
    [
        (StartsWith("Ab"), "Abel", False),
        (StartsWith("Ab"), "xyz", True),
        (EndsWith("com"), "test@example.com", False),
        (Regex(r"^$"), "", False),
        (Regex(r"^$"), "hello", True),
        # Non-string values
        (StartsWith("Ab"), 123, True),      # because inner returns False → Not = True
        (Regex(r".*"), None, True),
    ],
)
def test_not_parametrized(inner_predicate, value, expected):
    not_pred = Not(inner_predicate)
    assert not_pred.evaluate(value) is expected


# ====================== Nested Logical Combinations ======================

def test_nested_and_or(sample_value):
    """Complex nested logic: (starts with Ab OR ends with com) AND contains Ethiopia"""
    p = And(
        Or(
            StartsWith("Ab"),
            EndsWith("com")
        ),
        Regex(r"Ethiopia")
    )

    assert p.evaluate("Abel from Ethiopia") is True
    assert p.evaluate("test@example.com") is False          # no Ethiopia
    assert p.evaluate("Hello world from Ethiopia") is False # doesn't start with Ab nor end with com


def test_deep_nesting(sample_value):
    """Deeply nested: Not( And( Or(p1, p2), p3 ) )"""
    p = Not(
        And(
            Or(
                StartsWith("Ab"),
                EndsWith("com")
            ),
            Regex(r"example")
        )
    )

    assert p.evaluate("Abel@example.com") is False   # inner And is True → Not = False
    assert p.evaluate("xyz") is True                 # inner And is False → Not = True


# ====================== Serialization / Deserialization ======================

def test_and_serialization(sample_value, simple_predicates):
    original = And(
        simple_predicates["starts_ab"],
        simple_predicates["ends_com"],
        Not(simple_predicates["regex_abel"])
    )

    data = original.to_dict()

    assert data["type"] == "and"
    assert len(data["predicates"]) == 3

    loaded = Predicate.from_dict(data)
    assert isinstance(loaded, And)
    assert loaded == original

    # Verify behavior is preserved
    assert loaded.evaluate(sample_value["email"]) is False


def test_or_serialization(sample_value):
    original = Or(
        StartsWith("Ab"),
        Regex(r"example"),
        Not(EndsWith("xyz"))
    )

    loaded = Predicate.from_dict(original.to_dict())
    assert isinstance(loaded, Or)
    assert loaded == original
    assert loaded.evaluate("abel@example.com") is True


def test_not_serialization():
    original = Not(StartsWith("Ab"))
    loaded = Predicate.from_dict(original.to_dict())

    assert isinstance(loaded, Not)
    assert loaded == original
    assert loaded.evaluate("Abel") is False
    assert loaded.evaluate("xyz") is True


# ====================== Equality Tests ======================

def test_and_equality():
    p1 = And(StartsWith("Ab"), EndsWith("el"))
    p2 = And(StartsWith("Ab"), EndsWith("el"))
    p3 = And(StartsWith("Ab"), EndsWith("xyz"))

    assert p1 == p2
    assert p1 != p3
    assert p1 != "not a predicate"


def test_or_equality():
    p1 = Or(Regex(r"^A"), Regex(r"b$"))
    p2 = Or(Regex(r"^A"), Regex(r"b$"))
    p3 = Or(Regex(r"^A"), StartsWith("x"))

    assert p1 == p2
    assert p1 != p3


def test_not_equality():
    p1 = Not(StartsWith("Ab"))
    p2 = Not(StartsWith("Ab"))
    p3 = Not(EndsWith("el"))

    assert p1 == p2
    assert p1 != p3


def test_logical_equality_with_nested():
    nested1 = And(Or(StartsWith("A"), EndsWith("z")), Not(Regex(r"\d")))
    nested2 = And(Or(StartsWith("A"), EndsWith("z")), Not(Regex(r"\d")))
    nested3 = And(Or(StartsWith("A"), EndsWith("x")), Not(Regex(r"\d")))

    assert nested1 == nested2
    assert nested1 != nested3


# ====================== Error / Edge Cases ======================

def test_and_with_non_predicate_raises():
    """Passing non-Predicate objects should ideally fail early, but at least evaluate should be safe."""
    with pytest.raises(TypeError):  
        And("not a predicate", StartsWith("Ab"))


def test_or_with_non_predicate_raises():
    with pytest.raises(TypeError):
        Or(123, Regex(r".*"))


# ====================== Comprehensive Parametrized Coverage ======================

@pytest.mark.parametrize(
    "logic_type, predicates, value, expected",
    [
        # And cases
        ("and", [StartsWith("Ab"), EndsWith("el")], "Abel", True),
        ("and", [StartsWith("Ab"), EndsWith("com")], "Abel", False),
        ("and", [StartsWith(""), Regex(r".*")], "", True),
        # Or cases
        ("or", [StartsWith("xy"), EndsWith("el")], "Abel", True),
        ("or", [StartsWith("xy"), EndsWith("zz")], "Abel", False),
        ("or", [Regex(r"^$"), Regex(r"Abel")], "Abel", True),
        # Not cases
        ("not", [StartsWith("Ab")], "Abel", False),
        ("not", [EndsWith("com")], "test@example.com", False),
        ("not", [Regex(r"^$")], "hello", True),
    ],
)
def test_logical_combinations_parametrized(logic_type, predicates, value, expected):
    if logic_type == "and":
        pred = And(*predicates)
    elif logic_type == "or":
        pred = Or(*predicates)
    else:  # not
        pred = Not(predicates[0])

    assert pred.evaluate(value) is expected


def test_and_predicate():
    # age > 20 AND age == 25
    p1 = GreaterThan(20)
    p2 = Equals(25)
    logic = And(p1, p2)
    
    assert logic.evaluate(25) is True
    assert logic.evaluate(19) is False
    assert logic.evaluate(21) is False # Greater than 20 but not 25

def test_or_predicate():
    # age > 30 OR age == 25
    p1 = GreaterThan(30)
    p2 = Equals(25)
    logic = Or(p1, p2)
    
    assert logic.evaluate(31) is True
    assert logic.evaluate(25) is True
    assert logic.evaluate(20) is False

def test_not_predicate():
    # NOT (age == 25)
    p1 = Equals(25)
    logic = Not(p1)
    
    assert logic.evaluate(30) is True
    assert logic.evaluate(25) is False

def test_logical_equality():
    # Test __eq__ for And
    and1 = And(Equals(1), Equals(2))
    and2 = And(Equals(1), Equals(2))
    and3 = And(Equals(1))
    
    assert and1 == and2
    assert and1 != and3
    assert and1 != "not a predicate"

    # Test __eq__ for Not
    not1 = Not(Equals(1))
    not2 = Not(Equals(1))
    assert not1 == not2

def test_logical_serialization_roundtrip():
    # Complex nested: (age > 20 AND age < 30)
    original = And(GreaterThan(20), Equals(25))
    
    data = original.to_dict()
    from rules_engine.predicates.base import Predicate
    loaded = Predicate.from_dict(data)
    
    assert original == loaded
    assert isinstance(loaded, And)