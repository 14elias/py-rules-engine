from typing import Any, Dict, Type
from abc import ABC, abstractmethod


class Predicate(ABC):
    _registry: Dict[str, Type["Predicate"]] = {}

    @abstractmethod
    def evaluate(self, value: Any) -> bool:
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Predicate":
        if not isinstance(data, dict) or "type" not in data:
            raise ValueError("Predicate must have a 'type' field")

        pred_type = data["type"]

        if pred_type not in cls._registry:
            raise ValueError(f"Unknown predicate type: {pred_type}")

        return cls._registry[pred_type]._from_dict_impl(data)
    
    
    @classmethod
    @abstractmethod
    def _from_dict_impl(cls, data:Dict[str, Any]):
        pass

    
    @classmethod
    def register(cls, name: str):
        def decorator(subclass):
            cls._registry[name] = subclass
            subclass._type = name
            return subclass
        return decorator