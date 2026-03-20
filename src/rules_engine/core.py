from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass


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

    def parse_value(self, value: str):
        if value:
            return
    
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
        if self.field_name not in data:
            return False  # or raise KeyError? We'll decide later
        
        actual = data[self.field_name]
        
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