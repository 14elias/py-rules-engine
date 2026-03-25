from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Callable, Union, Pattern, Type, ClassVar
from dataclasses import dataclass
import json
import re


# ────────────────────────────────────────────────
#  Utility: Safe nested field access
# ────────────────────────────────────────────────
def get_nested(data: Any, path: str, default: Any = None) -> Any:
    """Safe dot-notation access. Returns original value if top-level is not dict."""
    if not path:
        return data

    if not isinstance(data, dict):
        return data  # Allow comparing scalar values directly

    current = data
    for key in path.split("."):
        if not isinstance(current, dict):
            return default
        current = current.get(key, default)
    return current


# ────────────────────────────────────────────────
#  Base Rule Class with Serialization
# ────────────────────────────────────────────────
class Rule(ABC):
    """Base class for all rules."""

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
        """Convert rule to JSON-serializable dictionary."""
        pass

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Rule':
        if not isinstance(data, dict) or "type" not in data:
            raise ValueError("Rule data must be a dict with 'type' key")

        rule_type = data["type"]
        if rule_type not in cls._registry:
            raise ValueError(f"Unknown rule type: {rule_type}")

        concrete_cls = cls._registry[rule_type]
        return concrete_cls._from_dict_impl(data)

    @classmethod
    @abstractmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'Rule':
        pass

    def to_json(self, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> 'Rule':
        data = json.loads(json_str)
        return cls.from_dict(data)

    # Operator overloading
    def __and__(self, other: 'Rule') -> 'AndRule':
        return AndRule(self, other)

    def __or__(self, other: 'Rule') -> 'OrRule':
        return OrRule(self, other)

    def __invert__(self) -> 'NotRule':
        return NotRule(self)

    def __repr__(self) -> str:
        raise NotImplementedError


# ────────────────────────────────────────────────
#  Composite Rules
# ────────────────────────────────────────────────

@Rule.register
@dataclass(frozen=True)
class AndRule(Rule):
    left: Rule
    right: Rule

    def evaluate(self, data: Any) -> bool:
        if not self.left.evaluate(data):
            return False
        return self.right.evaluate(data)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "AndRule",
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
        }

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'AndRule':
        return cls(
            left=Rule.from_dict(data["left"]),
            right=Rule.from_dict(data["right"]),
        )

    def __repr__(self) -> str:
        return f"And(\n  {self.left!r},\n  {self.right!r}\n)"


@Rule.register
@dataclass(frozen=True)
class OrRule(Rule):
    left: Rule
    right: Rule

    def evaluate(self, data: Any) -> bool:
        if self.left.evaluate(data):
            return True
        return self.right.evaluate(data)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "OrRule",
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
        }

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'OrRule':
        return cls(
            left=Rule.from_dict(data["left"]),
            right=Rule.from_dict(data["right"]),
        )

    def __repr__(self) -> str:
        return f"Or(\n  {self.left!r},\n  {self.right!r}\n)"


@Rule.register
@dataclass(frozen=True)
class NotRule(Rule):
    child: Rule

    def evaluate(self, data: Any) -> bool:
        return not self.child.evaluate(data)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "NotRule",
            "child": self.child.to_dict(),
        }

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'NotRule':
        return cls(child=Rule.from_dict(data["child"]))

    def __repr__(self) -> str:
        return f"Not({self.child!r})"


# ────────────────────────────────────────────────
#  ParenRule for explicit parentheses
# ────────────────────────────────────────────────

@Rule.register
@dataclass(frozen=True)
class ParenRule(Rule):
    child: Rule

    def evaluate(self, data: Any) -> bool:
        return self.child.evaluate(data)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "ParenRule",
            "child": self.child.to_dict(),
        }

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'ParenRule':
        return cls(child=Rule.from_dict(data["child"]))

    def __repr__(self) -> str:
        return f"({self.child!r})"


def P(rule: Rule) -> Rule:
    """Convenience function for explicit parentheses: P(A & B) | C"""
    return ParenRule(rule)


# ────────────────────────────────────────────────
#  Field & Comparison Rules
# ────────────────────────────────────────────────

@dataclass
class Field:
    name: str

    def __eq__(self, value: Any) -> 'ComparisonRule':
        return ComparisonRule(self.name, "==", value)

    def __ne__(self, value: Any) -> 'ComparisonRule':
        return ComparisonRule(self.name, "!=", value)

    def __gt__(self, value: Any) -> 'ComparisonRule':
        return ComparisonRule(self.name, ">", value)

    def __ge__(self, value: Any) -> 'ComparisonRule':
        return ComparisonRule(self.name, ">=", value)

    def __lt__(self, value: Any) -> 'ComparisonRule':
        return ComparisonRule(self.name, "<", value)

    def __le__(self, value: Any) -> 'ComparisonRule':
        return ComparisonRule(self.name, "<=", value)

    # Predicate methods
    def contains(self, value: Any) -> 'ContainsRule':
        return ContainsRule(self.name, value)

    def len(self) -> 'LengthProxy':
        return LengthProxy(self.name)

    def any(self, predicate: Callable[[Any], bool]) -> 'AnyRule':
        return AnyRule(self.name, predicate)

    def all(self, predicate: Callable[[Any], bool] | None = None) -> 'AllRule':
        if predicate is None:
            return AllRule(self.name, lambda x: x == self.name)  # Fixed: compare to value
        return AllRule(self.name, predicate)

    def startswith(self, prefix: str) -> 'StartsWithRule':
        return StartsWithRule(self.name, prefix)

    def matches(self, pattern: Union[str, Pattern]) -> 'RegexMatchRule':
        return RegexMatchRule(self.name, pattern)


@Rule.register
@dataclass(frozen=True)
class ComparisonRule(Rule):
    field_name: str
    operator: str
    value: Any

    def evaluate(self, data: Any) -> bool:
        actual = get_nested(data, self.field_name)
        if actual is None:
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
            "type": "ComparisonRule",
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

    def __repr__(self) -> str:
        return f"Field({self.field_name!r}) {self.operator} {self.value!r}"


# ────────────────────────────────────────────────
#  Predicate Rules
# ────────────────────────────────────────────────

@Rule.register
@dataclass(frozen=True)
class ContainsRule(Rule):
    field_name: str
    value: Any

    def evaluate(self, data: Any) -> bool:
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


@Rule.register
@dataclass(frozen=True)
class LengthComparisonRule(Rule):
    field_name: str
    operator: str
    length: int

    def evaluate(self, data: Any) -> bool:
        value = get_nested(data, self.field_name)
        if value is None:
            return False
        try:
            actual_len = len(value)
        except TypeError:
            return False

        if self.operator == "==": return actual_len == self.length
        if self.operator == "!=": return actual_len != self.length
        if self.operator == ">":  return actual_len > self.length
        if self.operator == ">=": return actual_len >= self.length
        if self.operator == "<":  return actual_len < self.length
        if self.operator == "<=": return actual_len <= self.length
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "LengthComparisonRule",
            "field": self.field_name,
            "op": self.operator,
            "length": self.length,
        }

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'LengthComparisonRule':
        return cls(
            field_name=data["field"],
            operator=data["op"],
            length=data["length"],
        )

    def __repr__(self) -> str:
        return f"Field({self.field_name!r}).len() {self.operator} {self.length}"


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


@Rule.register
@dataclass(frozen=True)
class StartsWithRule(Rule):
    field_name: str
    prefix: str

    def evaluate(self, data: Any) -> bool:
        value = get_nested(data, self.field_name)
        if not isinstance(value, str):
            return False
        return value.startswith(self.prefix)

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "StartsWithRule", "field": self.field_name, "prefix": self.prefix}

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'StartsWithRule':
        return cls(field_name=data["field"], prefix=data["prefix"])

    def __repr__(self) -> str:
        return f"Field({self.field_name!r}).startswith({self.prefix!r})"


@Rule.register
@dataclass(frozen=True)
class RegexMatchRule(Rule):
    field_name: str
    pattern: Union[str, Pattern]

    def __post_init__(self):
        if isinstance(self.pattern, str):
            object.__setattr__(self, "pattern", re.compile(self.pattern))

    def evaluate(self, data: Any) -> bool:
        value = get_nested(data, self.field_name)
        if not isinstance(value, str):
            return False
        return bool(self.pattern.search(value))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "RegexMatchRule",
            "field": self.field_name,
            "pattern": self.pattern.pattern if hasattr(self.pattern, "pattern") else self.pattern,
        }

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'RegexMatchRule':
        return cls(field_name=data["field"], pattern=data["pattern"])

    def __repr__(self) -> str:
        return f"Field({self.field_name!r}).matches({self.pattern!r})"


# ────────────────────────────────────────────────
#  LengthProxy
# ────────────────────────────────────────────────

@dataclass
class LengthProxy:
    field_name: str

    def __gt__(self, n: int) -> LengthComparisonRule:  return LengthComparisonRule(self.field_name, ">", n)
    def __ge__(self, n: int) -> LengthComparisonRule:  return LengthComparisonRule(self.field_name, ">=", n)
    def __lt__(self, n: int) -> LengthComparisonRule:  return LengthComparisonRule(self.field_name, "<", n)
    def __le__(self, n: int) -> LengthComparisonRule:  return LengthComparisonRule(self.field_name, "<=", n)
    def __eq__(self, n: int) -> LengthComparisonRule:  return LengthComparisonRule(self.field_name, "==", n)
    def __ne__(self, n: int) -> LengthComparisonRule:  return LengthComparisonRule(self.field_name, "!=", n)


# ────────────────────────────────────────────────
#  Example / Test
# ────────────────────────────────────────────────
if __name__ == "__main__":
    # Create complex rule
    rule = (
        ((Field("age") >= 18) & (Field("country") == "US")) |
        (Field("is_verified") == True)
    )

    print("Original Rule:", rule)

    # Serialize
    data_dict = rule.to_dict()
    json_str = rule.to_json()

    print("\nSerialized Dict:", json.dumps(data_dict, indent=2))
    print("\nSerialized JSON:", json_str)

    # Deserialize
    loaded_rule = Rule.from_dict(data_dict)
    loaded_from_json = Rule.from_json(json_str)

    # Test
    test_data = {"age": 25, "country": "ET", "is_verified": True}
    print("\nEvaluation after round-trip:", loaded_rule.evaluate(test_data))