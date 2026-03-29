from dataclasses import dataclass
from typing import Any, Dict
from rules_engine.core.base import Rule
from rules_engine.utils.nested import get_nested



@Rule.register("ComparisonRule")
@dataclass(frozen=True)
class ComparisonRule(Rule):
    field_name: str
    operator: str
    value: Any

    def evaluate(self, data: Any) -> bool:
        actual = get_nested(data, self.field_name)
        if actual is None:
            return False
        if type(actual) != type(self.value):
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
            "type": self._type,
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
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return (
            self.field_name == other.field_name and
            self.operator == other.operator and
            self.value == other.value
        )
        

    def __repr__(self) -> str:
        return f"Field({self.field_name!r}) {self.operator} {self.value!r}"