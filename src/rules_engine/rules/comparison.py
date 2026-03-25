from dataclasses import dataclass
from typing import Any, Dict
from ..core.base import Rule
from ..utils.nested import get_nested



@Rule.register
@dataclass(frozen=True)
class ComparisonRule(Rule):
    field_name: str
    operator: str
    value: Any

    def evaluate(self, data: Any) -> bool:
        actual = get_nested(data, self.field_name)
        if actual is None:
            return False

        if self.operator == "==": return actual == self.value
        if self.operator == "!=": return actual != self.value
        if self.operator == ">":  return actual > self.value
        if self.operator == ">=": return actual >= self.value
        if self.operator == "<":  return actual < self.value
        if self.operator == "<=": return actual <= self.value
        raise ValueError(f"Unknown operator: {self.operator}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "ComparisonRule",
            "field": self.field_name,
            "op": self.operator,
            "value": self.value,
        }

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'ComparisonRule':
        return cls(
            field_name=data["field"],
            operator=data["op"],
            value=data["value"],
        )

    def __repr__(self) -> str:
        return f"Field({self.field_name!r}) {self.operator} {self.value!r}"