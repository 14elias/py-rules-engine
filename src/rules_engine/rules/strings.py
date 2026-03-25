from dataclasses import dataclass
from typing import Any, Dict, Union, Pattern
import re
from ..core.base import Rule
from ..utils.nested import get_nested



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