from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Type, ClassVar
import json

class Rule(ABC):
    _registry: ClassVar[Dict[str, Type['Rule']]] = {}

    @classmethod
    def register(cls, subclass: Type['Rule']):
        cls._registry[subclass.__name__] = subclass
        return subclass

    @abstractmethod
    def evaluate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Rule':
        rule_type = data["type"]
        concrete_cls = cls._registry[rule_type]
        return concrete_cls._from_dict_impl(data)

    @classmethod
    @abstractmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'Rule':
        pass

    def to_json(self, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_json(cls, json_str: str) -> 'Rule':
        return cls.from_dict(json.loads(json_str))

    def __and__(self, other: 'Rule'):
        from .combinators import AndRule
        return AndRule(self, other)

    def __or__(self, other: 'Rule'):
        from .combinators import OrRule
        return OrRule(self, other)

    def __invert__(self):
        from .combinators import NotRule
        return NotRule(self)