from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass


def get_nested(data: Dict[str, Any], path: str, default=None) -> Any:
        current = data
        
        for key in path.split("."):
            if not isinstance(current, dict):
                return default
            current = current.get(key, default)
        return current


class Rule(ABC):
    """Base class for all rules."""
    @abstractmethod
    def evaluate(self, data: Dict[str, Any]) -> bool:
        """Evaluate this rule against the provided data."""
        pass

    def __and__(self, other) -> 'AndRule':
        return AndRule(self, other)
    
    def __or__(self, other) -> 'OrRule':
        return OrRule(self, other)
    
    def __invert__(self) -> 'NotRule':
        return NotRule(self)
    
    def __repr__(self) -> str:
        raise NotImplementedError




@dataclass(frozen=True)
class AndRule(Rule):
    left: Rule
    right: Rule

    def evaluate(self, context: Any) -> bool:
        # Short-circuit
        if not self.left.evaluate(context):
            return False
        return self.right.evaluate(context)

    def __repr__(self) -> str:
        return f"And(\n  {self.left!r},\n  {self.right!r}\n)"


@dataclass(frozen=True)
class OrRule(Rule):
    left: Rule
    right: Rule

    def evaluate(self, context: Any) -> bool:
        # Short-circuit
        if self.left.evaluate(context):
            return True
        return self.right.evaluate(context)

    def __repr__(self) -> str:
        return f"Or(\n  {self.left!r},\n  {self.right!r}\n)"


@dataclass(frozen=True)
class NotRule(Rule):
    child: Rule

    def evaluate(self, context: Any) -> bool:
        return not self.child.evaluate(context)

    def __repr__(self) -> str:
        return f"Not({self.child!r})"


@dataclass
class Field:
    """Represents a field in the data that can be compared."""
    
    name : str

    
    def __eq__(self, value: Any) -> 'ComparisonRule':
        return ComparisonRule(self.name, "==", value)
    
    def __ne__(self, value: Any) -> 'ComparisonRule':
        return ComparisonRule(self.name, "!=", value)
    
    def __gt__(self, value: Any) -> 'ComparisonRule':
        return ComparisonRule(self.name, ">", value)
    
    def __ge__(self, value: Any) -> 'ComparisonRule':
        return ComparisonRule(self.name, ">=", value)
    
    def __lt__(self, value: Any) -> 'ComparisonRule':
        return ComparisonRule(self.name, "<", value)
    
    def __le__(self, value: Any) -> 'ComparisonRule':
        return ComparisonRule(self.name, "<=", value)


    def contains(self, value: Any) -> 'ContainsRule':
        return ContainsRule(self.name, value)

    def len(self) -> 'LengthProxy':
        return LengthProxy(self.name)

    def any(self, predicate: Callable[[Any], bool]) -> 'AnyRule':
        return AnyRule(self.name, predicate)

    def all(self, predicate: Callable[[Any], bool] | None = None) -> 'AllRule':
        if predicate is None:
            # Field("roles").all() == "admin"  syntax sugar
            return AllRule(self.name, lambda x: x == self)  # self is the value!
        return AllRule(self.name, predicate)

    def startswith(self, prefix: str) -> 'StartsWithRule':
        return StartsWithRule(self.name, prefix)

    def matches(self, pattern: Union[str, Pattern]) -> 'RegexMatchRule':
        return RegexMatchRule(self.name, pattern)


@dataclass
class ComparisonRule(Rule):
    """Rule that compares a field against a value."""

    field_name: Field
    operator: str
    value: Any
    
    def __init__(self, field_name: str, operator: str, value: Any):
        self.field_name = field_name
        self.operator = operator
        self.value = value
    
    def evaluate(self, data: Dict[str, Any]) -> bool:

        actual = get_nested(data, self.field_name)
        if actual is None:
            return False
        
        if self.operator == "==":
            return actual == self.value
        elif self.operator == "!=":
            return actual != self.value
        elif self.operator == ">":
            return actual > self.value
        elif self.operator == ">=":
            return actual >= self.value
        elif self.operator == "<":
            return actual < self.value
        elif self.operator == "<=":
            return actual <= self.value
        else:
            raise ValueError(f"Unknown operator: {self.operator}")


from typing import Any, Callable, Pattern, Union
import re

# ────────────────────────────────────────
#  Collection / sequence predicates
# ────────────────────────────────────────

@dataclass(frozen=True)
class ContainsRule(Rule):
    field_name: str
    value: Any

    def evaluate(self, data: Any) -> bool:
        collection = get_nested(data, self.field_name)
        if collection is None:
            return False
        try:
            return self.value in collection
        except TypeError:  # not iterable
            return False


@dataclass(frozen=True)
class LengthComparisonRule(Rule):
    field_name: str
    operator: str
    length: int

    def evaluate(self, data: Any) -> bool:
        value = get_nested(data, self.field_name)
        if value is None:
            return False

        try:
            actual_len = len(value)
        except TypeError:
            return False

        if self.operator == "==": return actual_len == self.length
        if self.operator == "!=": return actual_len != self.length
        if self.operator == ">":  return actual_len >  self.length
        if self.operator == ">=": return actual_len >= self.length
        if self.operator == "<":  return actual_len <  self.length
        if self.operator == "<=": return actual_len <= self.length
        return False


@dataclass(frozen=True)
class AnyRule(Rule):
    field_name: str
    predicate: Callable[[Any], bool]

    def evaluate(self, data: Any) -> bool:
        collection = get_nested(data, self.field_name)
        if not isinstance(collection, (list, tuple, set)):
            return False
        return any(self.predicate(item) for item in collection)


@dataclass(frozen=True)
class AllRule(Rule):
    field_name: str
    predicate: Callable[[Any], bool]

    def evaluate(self, data: Any) -> bool:
        collection = get_nested(data, self.field_name)
        if not isinstance(collection, (list, tuple, set)):
            return False
        return all(self.predicate(item) for item in collection) if collection else False


@dataclass(frozen=True)
class StartsWithRule(Rule):
    field_name: str
    prefix: str

    def evaluate(self, data: Any) -> bool:
        value = get_nested(data, self.field_name)
        if not isinstance(value, str):
            return False
        return value.startswith(self.prefix)


@dataclass(frozen=True)
class RegexMatchRule(Rule):
    field_name: str
    pattern: Union[str, Pattern]

    def __post_init__(self):
        if isinstance(self.pattern, str):
            object.__setattr__(self, "pattern", re.compile(self.pattern))

    def evaluate(self, data: Any) -> bool:
        value = get_nested(data, self.field_name)
        if not isinstance(value, str):
            return False
        return bool(self.pattern.search(value))


@dataclass
class LengthProxy:
    """Helper so Field('items').len() > 5 works"""
    field_name: str

    def __gt__(self, n: int)  -> LengthComparisonRule: 
        return LengthComparisonRule(self.field_name, ">",  n)
    
    def __ge__(self, n: int)  -> LengthComparisonRule:
        return LengthComparisonRule(self.field_name, ">=", n)
    
    def __lt__(self, n: int)  -> LengthComparisonRule: 
        return LengthComparisonRule(self.field_name, "<",  n)
    
    def __le__(self, n: int)  -> LengthComparisonRule: 
        return LengthComparisonRule(self.field_name, "<=", n)
    
    def __eq__(self, n: int)  -> LengthComparisonRule: 
        return LengthComparisonRule(self.field_name, "==", n)
    
    def __ne__(self, n: int)  -> LengthComparisonRule: 
        return LengthComparisonRule(self.field_name, "!=", n)



if __name__ == "__main__":

    from .resolvers import P
    # Create rules
    age_rule = Field("age") >= 18
    country_rule = Field("country") == "US"
    verified_rule = Field("is_verified") == True
    
    # Combine them
    final_rule = (age_rule | country_rule) & verified_rule
    final_rule2 = P(verified_rule & age_rule) | country_rule
    # Test data
    user1 = {"age": 19, "country": "US", "is_verified": False}
    user2 = {"age": 19, "country": "US", "is_verified": False}
    
    print(f"User1: {final_rule.evaluate(user1)}")  # True (age & country pass)
    print(f"User2: {final_rule2.evaluate(user2)}")  # True (verified passes)
    data = {"user": {"profile": {"age": 25}}}
    rule3 = (Field("user.profile.age") >= 18).evaluate(data)
    print(f"data: {rule3}")