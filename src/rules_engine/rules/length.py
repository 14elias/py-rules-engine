from dataclasses import dataclass
from typing import Any, Dict
from ..core.base import Rule
from ..utils.nested import get_nested


@Rule.register
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
        if self.operator == ">":  return actual_len > self.length
        if self.operator == ">=": return actual_len >= self.length
        if self.operator == "<":  return actual_len < self.length
        if self.operator == "<=": return actual_len <= self.length
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "LengthComparisonRule",
            "field": self.field_name,
            "op": self.operator,
            "length": self.length,
        }

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'LengthComparisonRule':
        return cls(
            field_name=data["field"],
            operator=data["op"],
            length=data["length"],
        )

    def __repr__(self) -> str:
        return f"Field({self.field_name!r}).len() {self.operator} {self.length}"