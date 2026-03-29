from dataclasses import dataclass
from typing import Any, Dict, Union, Pattern
import re
from rules_engine.core.base import Rule
from rules_engine.utils.nested import get_nested



@Rule.register("StartsWithRule")
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
        return {"type": self._type, "field": self.field_name, "prefix": self.prefix}

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'StartsWithRule':
        return cls(field_name=data["field"], prefix=data["prefix"])
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return (
            self.field_name == other.field_name and
            self.prefix == other.prefix
        )

    def __repr__(self) -> str:
        return f"Field({self.field_name!r}).startswith({self.prefix!r})"



@Rule.register("EndsWithRule")
@dataclass(frozen=True)
class EndsWithRule(Rule):
    field_name: str
    suffix: str

    def evaluate(self, data: Any) -> bool:
        value = get_nested(data, self.field_name)
        if not isinstance(value, str):
            return False
        return value.endswith(self.suffix)

    def to_dict(self) -> Dict[str, Any]:
        return {"type": self._type, "field": self.field_name, "suffix": self.suffix}

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'EndsWithRule':
        return cls(field_name=data["field"], suffix=data["suffix"])
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return (
            self.field_name == other.field_name and
            self.suffix == other.suffix
        )

    def __repr__(self) -> str:
        return f"Field({self.field_name!r}).endswith({self.suffix!r})"


@Rule.register("RegexMatchRule")
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
            "type": self._type,
            "field": self.field_name,
            "pattern": self.pattern.pattern if hasattr(self.pattern, "pattern") else self.pattern,
        }

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'RegexMatchRule':
        return cls(field_name=data["field"], pattern=data["pattern"])
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        self_p = self.pattern.pattern if hasattr(self.pattern, "pattern") else self.pattern
        other_p = other.pattern.pattern if hasattr(other.pattern, "pattern") else other.pattern
        return self.field_name == other.field_name and self_p == other_p

    def __repr__(self) -> str:
        return f"Field({self.field_name!r}).matches({self.pattern!r})"