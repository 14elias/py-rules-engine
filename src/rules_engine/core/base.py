from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Type, ClassVar
import json



class Rule(ABC):
    _registry: ClassVar[Dict[str, Type['Rule']]] = {}

    @classmethod
    def register(cls, name: str):
        """Decorator that registers a rule class under a specific string name."""
        def wrapper(subclass: Type['Rule']):
            cls._registry[name] = subclass
            subclass._type = name
            return subclass
        return wrapper

    @abstractmethod
    def evaluate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Rule':
        if not isinstance(data, dict) or "type" not in data:
            raise ValueError("Rule data must be a dict with 'type' key")
        
        if not cls._registry:
            cls._discover_rules()

        rule_type = data["type"]

        print(f"\nDEBUG: Looking for {rule_type}")
        print(f"DEBUG: Registry content: {list(cls._registry.keys())}")
        print(f"DEBUG: Registry ID: {id(cls._registry)}")

        if rule_type not in cls._registry:
                raise ValueError(f"Unknown rule type: {rule_type}")
        concrete_cls = cls._registry[rule_type]
        return concrete_cls._from_dict_impl(data)
    

    @staticmethod
    def _discover_rules():
        import importlib
        import pkgutil
        import rules_engine.rules as rules_pkg
        import rules_engine.core.combinators # explicitly import this too

        # Automatically find and import all modules in the rules directory
        package = rules_pkg.__name__

        for _, module_name, _ in pkgutil.iter_modules(rules_pkg.__path__):
            importlib.import_module(f"{package}.{module_name}")


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
    
        