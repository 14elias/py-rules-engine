from dataclasses import dataclass
from typing import Any, Dict
from rules_engine.core.base import Rule
from rules_engine.utils.nested import get_nested


@Rule.register("LengthComparisonRule")
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
            "type": self._type,
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
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return (
            self.field_name == other.field_name and
            self.operator == other.operator and
            self.length == other.length
        )

    def __repr__(self) -> str:
        return f"Field({self.field_name!r}).len() {self.operator} {self.length}"