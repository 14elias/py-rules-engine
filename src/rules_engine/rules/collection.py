from dataclasses import dataclass
from typing import Any, Dict, Union, Pattern, Callable
from ..core.base import Rule
from ..utils.nested import get_nested


@Rule.register
@dataclass(frozen=True)
class AnyRule(Rule):
    field_name: str
    predicate: Callable[[Any], bool]

    def evaluate(self, data: Any) -> bool:
        collection = get_nested(data, self.field_name)
        if not isinstance(collection, (list, tuple, set)):
            return False
        return any(self.predicate(item) for item in collection)

    def to_dict(self) -> Dict[str, Any]:
        # Note: Lambdas cannot be serialized easily. Store as string or restrict usage.
        raise NotImplementedError("AnyRule with arbitrary predicate cannot be serialized safely.")

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'AnyRule':
        raise NotImplementedError("Deserializing AnyRule with predicate is not supported.")


@Rule.register
@dataclass(frozen=True)
class AllRule(Rule):
    field_name: str
    predicate: Callable[[Any], bool]

    def evaluate(self, data: Any) -> bool:
        collection = get_nested(data, self.field_name)
        if not isinstance(collection, (list, tuple, set)):
            return False
        return all(self.predicate(item) for item in collection) if collection else False

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError("AllRule with arbitrary predicate cannot be serialized safely.")

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'AllRule':
        raise NotImplementedError("Deserializing AllRule with predicate is not supported.")