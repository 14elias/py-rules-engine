from dataclasses import dataclass
from typing import Any, Dict

from rules_engine.core.base import Rule
from rules_engine.utils.nested import get_nested


@Rule.register("ComparisonRule")
@dataclass(frozen=True)
class ComparisonRule(Rule):
    """A rule that compares a field's value using a comparison operator.

    This is the core rule used when using operators on `Field` such as:
    `==`, `!=`, `>`, `>=`, `<`, `<=`.

    Examples:
        Field("age") >= 18
        Field("status") == "active"
        Field("score") < 100
    """

    field_name: str
    """The name of the field to compare (supports dot notation for nested fields)."""

    operator: str
    """The comparison operator. One of: '==', '!=', '>', '>=', '<', '<='."""

    value: Any
    """The value to compare the field against."""

    def evaluate(self, data: Any) -> bool:
        """Evaluate the comparison against the provided data.

        Note:
            - Returns False if the field is missing or None.
            - Returns False if the actual value and comparison value 
            have different types.
        """

        actual = get_nested(data, self.field_name)
        if actual is None:
            return False
        if type(actual) is not type(self.value):
            return False

        if self.operator == "==": 
            return actual == self.value
        if self.operator == "!=": 
            return actual != self.value
        if self.operator == ">":  
            return actual > self.value
        if self.operator == ">=": 
            return actual >= self.value
        if self.operator == "<":  
            return actual < self.value
        if self.operator == "<=": 
            return actual <= self.value
        raise ValueError(f"Unknown operator: {self.operator}")

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the rule to a dictionary."""

        return {
            "type": self._type,
            "field": self.field_name,
            "op": self.operator,
            "value": self.value,
        }

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'ComparisonRule':
        """Deserialize from dictionary representation."""

        return cls(
            field_name=data["field"],
            operator=data["op"],
            value=data["value"],
        )
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return (
            self.field_name == other.field_name and
            self.operator == other.operator and
            self.value == other.value
        )
        

    def __repr__(self) -> str:
        """Return a readable string representation of the rule."""

        return f"Field({self.field_name!r}) {self.operator} {self.value!r}"