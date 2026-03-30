from dataclasses import dataclass
from typing import Any, Union, Pattern
from rules_engine.rules.comparison import ComparisonRule
from rules_engine.rules.contains import ContainsRule
from rules_engine.rules.length import LengthComparisonRule
from rules_engine.rules.strings import StartsWithRule, RegexMatchRule, EndsWithRule
from rules_engine.rules.collection import AnyRule, AllRule
from rules_engine.predicates.base import Predicate



@dataclass
class Field:
    """Represents a field in the data that can be used to build rules.

    The `Field` class is the main entry point for building rules in a fluent,
    Pythonic way. It supports comparison operators and common predicate methods.

    Examples:
        >>> from rules_engine import Field
        >>> 
        >>> age = Field("age")
        >>> rule = (age >= 18) & (Field("role") == "admin")
        >>> 
        >>> profile_age = Field("profile.age")
    """

    name: str
    """The name of the field, supporting dot notation for nested access (e.g. 'profile.age')."""

    def __eq__(self, value: Any) -> 'ComparisonRule':
        """Return a rule that checks if this field equals the given value."""
        return ComparisonRule(self.name, "==", value)

    def __ne__(self, value: Any) -> 'ComparisonRule':
        """Return a rule that checks if this field is not equal to the given value."""
        return ComparisonRule(self.name, "!=", value)

    def __gt__(self, value: Any) -> 'ComparisonRule':
        """Return a rule that checks if this field is greater than the given value."""
        return ComparisonRule(self.name, ">", value)

    def __ge__(self, value: Any) -> 'ComparisonRule':
        """Return a rule that checks if this field is greater than or equal to the given value."""
        return ComparisonRule(self.name, ">=", value)

    def __lt__(self, value: Any) -> 'ComparisonRule':
        """Return a rule that checks if this field is less than the given value."""
        return ComparisonRule(self.name, "<", value)

    def __le__(self, value: Any) -> 'ComparisonRule':
        """Return a rule that checks if this field is less than or equal to the given value."""
        return ComparisonRule(self.name, "<=", value)

    # Predicate methods
    def contains(self, value: Any) -> 'ContainsRule':
        """Return a rule that checks if this field contains the given value.

        Works with strings and collections.
        """
        return ContainsRule(self.name, value)

    def len(self) -> 'LengthProxy':
        """Return a proxy object to compare the length of this field.

        Example:
            Field("tags").len() >= 5
        """
        return LengthProxy(self.name)

    def any(self, predicate: Predicate) -> 'AnyRule':
        """Return a rule that checks if ANY item in the collection satisfies the predicate.

        Args:
            predicate: A Predicate instance to apply to each item.

        Example:
            Field("roles").any(Equals("admin"))
        """
        return AnyRule(self.name, predicate)

    def all(self, predicate: Predicate) -> 'AllRule':
        """Return a rule that checks if ALL items in the collection satisfy the predicate."""
        return AllRule(self.name, predicate)

    def startswith(self, prefix: str) -> 'StartsWithRule':
        """Return a rule that checks if this field starts with the given prefix (string only)."""
        return StartsWithRule(self.name, prefix)
    
    def endswith(self, suffix: str) -> 'StartsWithRule':
        """Return a rule that checks if this field ends with the given suffix (string only)."""
        return EndsWithRule(self.name, suffix)

    def matches(self, pattern: Union[str, Pattern]) -> 'RegexMatchRule':
        """Return a rule that checks if this field matches the given regex pattern."""
        return RegexMatchRule(self.name, pattern)



@dataclass
class LengthProxy:
    """Proxy class returned by `Field.len()` to support length comparisons.

    This class allows natural syntax like `Field("tags").len() >= 3`.
    """

    field_name: str
    """Name of the field whose length is being compared."""

    def __gt__(self, n: int) -> LengthComparisonRule:  
        return LengthComparisonRule(self.field_name, ">", n)
    
    def __ge__(self, n: int) -> LengthComparisonRule:  
        return LengthComparisonRule(self.field_name, ">=", n)
    
    def __lt__(self, n: int) -> LengthComparisonRule:  
        return LengthComparisonRule(self.field_name, "<", n)
    
    def __le__(self, n: int) -> LengthComparisonRule:  
        return LengthComparisonRule(self.field_name, "<=", n)
    
    def __eq__(self, n: int) -> LengthComparisonRule:  
        return LengthComparisonRule(self.field_name, "==", n)
    
    def __ne__(self, n: int) -> LengthComparisonRule:  
        return LengthComparisonRule(self.field_name, "!=", n)



