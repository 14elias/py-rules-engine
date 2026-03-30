from dataclasses import dataclass
from typing import Any, Dict

from rules_engine.core.base import Rule
from rules_engine.predicates.base import Predicate
from rules_engine.utils.nested import get_nested


@Rule.register("AnyRule")
@dataclass(frozen=True)
class AnyRule(Rule):
    """Rule that returns True if ANY item in a collection satisfies the given predicate.

    Example:
        Field("roles").any(Equals("admin"))   
    """

    field_name: str
    predicate: Predicate

    def __post_init__(self):
        if not isinstance(self.predicate, Predicate):
            raise TypeError(
                f'any argument to AnyRule() must be predicate instance '
                f"Got {type(self.predicate).__name__}"
            )

    def evaluate(self, data: Any) -> bool:
        collection = get_nested(data, self.field_name)
        if not isinstance(collection, (list, tuple, set)):
            return False

        return any(self.predicate.evaluate(item) for item in collection)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self._type,
            "field": self.field_name,
            "predicate": self.predicate.to_dict()
        }

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'AnyRule':
        return cls(
            field_name=data["field"],
            predicate=Predicate.from_dict(data["predicate"])
        )

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return self.field_name == other.field_name and self.predicate == other.predicate


@Rule.register("AllRule")
@dataclass(frozen=True)
class AllRule(Rule):
    """Rule that returns True if ALL items in a collection satisfy 
    the given predicate."""

    field_name: str
    predicate: Predicate

    def __post_init__(self):
        if not isinstance(self.predicate, Predicate):
            raise TypeError(
                f'any argument to AllRule() must be predicate instance '
                f"Got {type(self.predicate).__name__}"
            )

    def evaluate(self, data: Any) -> bool:
        collection = get_nested(data, self.field_name)
        if not isinstance(collection, (list, tuple, set)):
            return False
        if collection:
            return all(self.predicate.evaluate(item) for item in collection)
        else : 
            return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self._type,
            "field": self.field_name,
            "predicate": self.predicate.to_dict()
        }

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'AllRule':
        return cls(
            field_name=data["field"],
            predicate=Predicate.from_dict(data["predicate"])
        )
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return self.field_name == other.field_name and self.predicate == other.predicate