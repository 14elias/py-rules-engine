from abc import ABC, abstractmethod
from typing import Any, Dict, Type


class Predicate(ABC):
    """Abstract base class for all predicates.

    Predicates are used primarily with collection rules like `.any()` and `.all()`
    to define conditions that should be applied to individual items in a list.

    This system mirrors the main `Rule` class but operates on single values instead of
    entire data dicts.
    """

    _registry: Dict[str, Type["Predicate"]] = {}

    @abstractmethod
    def evaluate(self, value: Any) -> bool:
        """Evaluate this predicate against a single value.

        Args:
            value: The individual item to test.

        Returns:
            True if the predicate passes for the given value.
        """

        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert the predicate to a dictionary for serialization."""

        pass

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Predicate":
        """Reconstruct a Predicate from its dictionary representation."""

        if not isinstance(data, dict) or "type" not in data:
            raise ValueError("Predicate must have a 'type' field")

        pred_type = data["type"]

        if pred_type not in cls._registry:
            raise ValueError(f"Unknown predicate type: {pred_type}")

        return cls._registry[pred_type]._from_dict_impl(data)

    @classmethod
    @abstractmethod
    def _from_dict_impl(cls, data: Dict[str, Any]):
        """Internal deserialization method implemented by concrete predicate classes."""

        pass

    @classmethod
    def register(cls, name: str):
        """Decorator to register a predicate class in the global registry."""

        def decorator(subclass):
            cls._registry[name] = subclass
            subclass._type = name
            return subclass

        return decorator
