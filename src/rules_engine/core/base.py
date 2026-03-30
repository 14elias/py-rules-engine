from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any, ClassVar, Dict, Type


class Rule(ABC):
    """Abstract base class for all rules in the rules-engine.

    This is the core class of the library. All rules (comparison, logical,
    string, collection, etc.) inherit from `Rule`.

    Rules support:
      - Evaluation against data (`evaluate()`)
      - JSON serialization (`to_dict()`, `to_json()`)
      - Deserialization (`from_dict()`, `from_json()`)
      - Composition using Python operators: `&` (AND), `|` (OR), `~` (NOT)
    """

    _registry: ClassVar[Dict[str, Type["Rule"]]] = {}

    @classmethod
    def register(cls, name: str):
        """Decorator to register a rule class in the global registry.

        This enables proper deserialization via `Rule.from_dict()` and
        `Rule.from_json()`.
        """

        def wrapper(subclass: Type["Rule"]):
            cls._registry[name] = subclass
            subclass._type = name
            return subclass

        return wrapper

    @abstractmethod
    def evaluate(self, data: Any) -> bool:
        """Evaluate this rule against the given data.

        Args:
            data: The data (usually a dict) to evaluate the rule against.

        Returns:
            True if the rule passes, False otherwise.
        """

        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert this rule to a dictionary representation for serialization."""

        pass

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Rule":
        """Reconstruct a Rule instance from its dictionary representation.

        This method automatically discovers registered rule types if needed.

        Raises:
            ValueError: If the data is invalid or the rule type is unknown.
        """

        if not isinstance(data, dict) or "type" not in data:
            raise ValueError("Rule data must be a dict with 'type' key")

        if not cls._registry:
            cls._discover_rules()

        rule_type = data["type"]

        if rule_type not in cls._registry:
            raise ValueError(f"Unknown rule type: {rule_type}")
        concrete_cls = cls._registry[rule_type]
        return concrete_cls._from_dict_impl(data)

    @staticmethod
    def _discover_rules():
        """Internal method to discover and import all rule modules."""

        import importlib
        import pkgutil

        import rules_engine.rules as rules_pkg

        # Automatically find and import all modules in the rules directory
        package = rules_pkg.__name__

        for _, module_name, _ in pkgutil.iter_modules(rules_pkg.__path__):
            importlib.import_module(f"{package}.{module_name}")

    @classmethod
    @abstractmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> "Rule":
        """Internal method implemented by concrete rule classes for deserialization."""

        pass

    def to_json(self, indent: int | None = 2) -> str:
        """Convert this rule to a formatted JSON string."""

        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_json(cls, json_str: str) -> "Rule":
        """Reconstruct a Rule from a JSON string."""

        return cls.from_dict(json.loads(json_str))

    def __and__(self, other: "Rule"):
        """Combine this rule with another using logical AND."""

        from .combinators import AndRule

        return AndRule(self, other)

    def __or__(self, other: "Rule"):
        """Combine this rule with another using logical OR."""

        from .combinators import OrRule

        return OrRule(self, other)

    def __invert__(self):
        """Return the logical negation of this rule (NOT)."""

        from .combinators import NotRule

        return NotRule(self)
