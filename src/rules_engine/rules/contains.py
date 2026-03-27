from dataclasses import dataclass
from typing import Any, Dict
from ..core.base import Rule
from ..utils.nested import get_nested



@Rule.register
@dataclass(frozen=True)
class ContainsRule(Rule):
    field_name: str
    value: Any

    def evaluate(self, data: Any) ->  bool:
        collection = get_nested(data, self.field_name)
        if collection is None:
            return False
        try:
            return self.value in collection
        except TypeError:
            return False

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "ContainsRule", "field": self.field_name, "value": self.value}

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'ContainsRule':
        return cls(field_name=data["field"], value=data["value"])

    def __repr__(self) -> str:
        return f"Field({self.field_name!r}).contains({self.value!r})"