import re
from dataclasses import dataclass
from typing import Any, Dict, Pattern, Union

from rules_engine.core.base import Rule
from rules_engine.utils.nested import get_nested


@Rule.register("StartsWithRule")
@dataclass(frozen=True)
class StartsWithRule(Rule):
    """Rule that checks if a field's string value starts with a given prefix.

    Example:
        Field("username").startswith("guest_")
    """

    field_name: str
    """Name of the field to check."""

    prefix: str
    """The prefix string that the field value must start with."""

    def evaluate(self, data: Any) -> bool:
        """Evaluate whether the field starts with the specified prefix.

        Returns False if the field is missing or not a string.
        """

        value = get_nested(data, self.field_name)
        if not isinstance(value, str):
            return False
        return value.startswith(self.prefix)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the rule to a dictionary."""

        return {"type": self._type, "field": self.field_name, "prefix": self.prefix}

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> "StartsWithRule":
        """Deserialize from dictionary."""

        return cls(field_name=data["field"], prefix=data["prefix"])

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.field_name == other.field_name and self.prefix == other.prefix

    def __repr__(self) -> str:
        """Return a readable representation using Field.startswith() syntax."""

        return f"Field({self.field_name!r}).startswith({self.prefix!r})"


@Rule.register("EndsWithRule")
@dataclass(frozen=True)
class EndsWithRule(Rule):
    """Rule that checks if a field's string value ends with a given suffix.

    Example:
        Field("filename").endswith(".pdf")
    """

    field_name: str
    """Name of the field to check."""

    suffix: str
    """The suffix string that the field value must start with."""

    def evaluate(self, data: Any) -> bool:
        """Evaluate whether the field ends with the specified suffix.

        Returns False if the field is missing or not a string.
        """

        value = get_nested(data, self.field_name)
        if not isinstance(value, str):
            return False
        return value.endswith(self.suffix)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the rule to a dictionary."""

        return {"type": self._type, "field": self.field_name, "suffix": self.suffix}

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> "EndsWithRule":
        """Deserialize from dictionary."""

        return cls(field_name=data["field"], suffix=data["suffix"])

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.field_name == other.field_name and self.suffix == other.suffix

    def __repr__(self) -> str:
        """Return a readable representation using Field.endswith() syntax."""

        return f"Field({self.field_name!r}).endswith({self.suffix!r})"


@Rule.register("RegexMatchRule")
@dataclass(frozen=True)
class RegexMatchRule(Rule):
    """Rule that checks if a field's string value matches a regular expression pattern.

    The pattern is compiled once during initialization for better performance.

    Example:
        Field("email").matches(r".+@company\.com$")
    """

    field_name: str
    """Name of the field to check."""

    pattern: Union[str, Pattern]
    """The regex pattern (string or pre-compiled Pattern object)."""

    def __post_init__(self):
        if isinstance(self.pattern, str):
            object.__setattr__(self, "pattern", re.compile(self.pattern))

    def evaluate(self, data: Any) -> bool:
        """Evaluate whether the field matches the regex pattern.

        Returns False if the field is missing or not a string.
        """

        value = get_nested(data, self.field_name)
        if not isinstance(value, str):
            return False
        return bool(self.pattern.search(value))

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the rule (stores the pattern string)."""
        pattern = None
        if hasattr(self.pattern, "pattern"):
            pattern = self.pattern.pattern
        else:
            pattern = self.pattern

        return {
            "type": self._type,
            "field": self.field_name,
            "pattern": pattern,
        }

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> "RegexMatchRule":
        """Deserialize from dictionary."""

        return cls(field_name=data["field"], pattern=data["pattern"])

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        self_p = None
        other_p = None

        if hasattr(self.pattern, "pattern"):
            self_p = self.pattern.pattern
        else:
            self_p = self.pattern

        if hasattr(other.pattern, "pattern"):
            other_p = other.pattern.pattern
        else:
            other_p = other.pattern

        return self.field_name == other.field_name and self_p == other_p

    def __repr__(self) -> str:
        """Return a readable representation using Field.matches() syntax."""

        return f"Field({self.field_name!r}).matches({self.pattern!r})"
