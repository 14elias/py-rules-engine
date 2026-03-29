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

    def any(self, predicate: Predicate) -> 'AnyRule':
        return AnyRule(self.name, predicate)

    def all(self, predicate: Predicate) -> 'AllRule':
        return AllRule(self.name, predicate)

    def startswith(self, prefix: str) -> 'StartsWithRule':
        return StartsWithRule(self.name, prefix)
    
    def endswith(self, suffix: str) -> 'StartsWithRule':
        return EndsWithRule(self.name, suffix)

    def matches(self, pattern: Union[str, Pattern]) -> 'RegexMatchRule':
        return RegexMatchRule(self.name, pattern)



@dataclass
class LengthProxy:
    field_name: str

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



