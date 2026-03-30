from dataclasses import dataclass
from typing import Any, Dict

from rules_engine.core.base import Rule
from rules_engine.utils.nested import get_nested


@Rule.register("LengthComparisonRule")
@dataclass(frozen=True)
class LengthComparisonRule(Rule):
    """Rule that compares the length of a field's value.

    This rule is created when using `.len()` on a Field, for example:
        Field("tags").len() >= 5
        Field("orders").len() == 0

    Supports all comparison operators: ==, !=, >, >=, <, <=
    """

    field_name: str
    """Name of the field whose length will be compared."""

    operator: str
    """Comparison operator. One of: '==', '!=', '>', '>=', '<', '<='."""

    length: int
    """The length value to compare against."""

    def evaluate(self, data: Any) -> bool:
        """Evaluate the length comparison.

        Note:
            Returns False if the field is missing, None, or not a 
            sized collection/string.
        """

        value = get_nested(data, self.field_name)
        if value is None:
            return False
        try:
            actual_len = len(value)
        except TypeError:
            return False

        if self.operator == "==": 
            return actual_len == self.length
        if self.operator == "!=": 
            return actual_len != self.length
        if self.operator == ">":  
            return actual_len > self.length
        if self.operator == ">=": 
            return actual_len >= self.length
        if self.operator == "<":  
            return actual_len < self.length
        if self.operator == "<=": 
            return actual_len <= self.length
        return False

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the length comparison rule."""

        return {
            "type": self._type,
            "field": self.field_name,
            "op": self.operator,
            "length": self.length,
        }

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'LengthComparisonRule':
        """Deserialize from dictionary."""

        return cls(
            field_name=data["field"],
            operator=data["op"],
            length=data["length"],
        )
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return (
            self.field_name == other.field_name and
            self.operator == other.operator and
            self.length == other.length
        )

    def __repr__(self) -> str:
        """Return a readable string representation."""

        return f"Field({self.field_name!r}).len() {self.operator} {self.length}"