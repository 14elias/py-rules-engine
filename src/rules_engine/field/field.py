from dataclasses import dataclass
from typing import Any, Dict, Callable, Union, Pattern, Type, ClassVar
from ..rules.comparison import ComparisonRule
from ..rules.contains import ContainsRule
from ..rules.length import LengthComparisonRule
from ..rules.strings import StartsWithRule, RegexMatchRule
from ..rules.collection import AnyRule, AllRule



@dataclass
class Field:
    name: str

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

    # Predicate methods
    def contains(self, value: Any) -> 'ContainsRule':
        return ContainsRule(self.name, value)

    def len(self) -> 'LengthProxy':
        return LengthProxy(self.name)

    def any(self, predicate: Callable[[Any], bool]) -> 'AnyRule':
        return AnyRule(self.name, predicate)

    def all(self, predicate: Callable[[Any], bool] | None = None) -> 'AllRule':
        if predicate is None:
            return AllRule(self.name, lambda x: x == self.name)  # Fixed: compare to value
        return AllRule(self.name, predicate)

    def startswith(self, prefix: str) -> 'StartsWithRule':
        return StartsWithRule(self.name, prefix)

    def matches(self, pattern: Union[str, Pattern]) -> 'RegexMatchRule':
        return RegexMatchRule(self.name, pattern)



@dataclass
class LengthProxy:
    field_name: str

    def __gt__(self, n: int) -> LengthComparisonRule:  return LengthComparisonRule(self.field_name, ">", n)
    def __ge__(self, n: int) -> LengthComparisonRule:  return LengthComparisonRule(self.field_name, ">=", n)
    def __lt__(self, n: int) -> LengthComparisonRule:  return LengthComparisonRule(self.field_name, "<", n)
    def __le__(self, n: int) -> LengthComparisonRule:  return LengthComparisonRule(self.field_name, "<=", n)
    def __eq__(self, n: int) -> LengthComparisonRule:  return LengthComparisonRule(self.field_name, "==", n)
    def __ne__(self, n: int) -> LengthComparisonRule:  return LengthComparisonRule(self.field_name, "!=", n)