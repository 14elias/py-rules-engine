from dataclasses import dataclass
from typing import Any, Dict, Union, Pattern, Callable
from rules_engine.core.base import Rule
from rules_engine.utils.nested import get_nested
from rules_engine.predicates.base import Predicate



@Rule.register
@dataclass(frozen=True)
class AnyRule(Rule):
    field_name: str
    predicate: Predicate

    def evaluate(self, data: Any) -> bool:
        collection = get_nested(data, self.field_name)
        if not isinstance(collection, (list, tuple, set)):
            return False
        return any(self.predicate.evaluate(item) for item in collection)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "AnyRule",
            "field": self.field,
            "predicate": self.predicate.to_dict()
        }

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'AnyRule':
        return cls(
            field=data["field"],
            predicate=Predicate.from_dict(data["predicate"])
        )


@Rule.register
@dataclass(frozen=True)
class AllRule(Rule):
    field_name: str
    predicate: Predicate

    def evaluate(self, data: Any) -> bool:
        collection = get_nested(data, self.field_name)
        if not isinstance(collection, (list, tuple, set)):
            return False
        return all(self.predicate.evaluate(item) for item in collection) if collection else False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "AllRule",
            "field": self.field,
            "predicate": self.predicate.to_dict()
        }

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'AllRule':
        return cls(
            field=data["field"],
            predicate=Predicate.from_dict(data["predicate"])
        )