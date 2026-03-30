from dataclasses import dataclass
from typing import Any, Dict

from rules_engine.core.base import Rule
from rules_engine.utils.nested import get_nested


@Rule.register("ContainsRule")
@dataclass(frozen=True)
class ContainsRule(Rule):
    """Rule that checks whether a field's value contains a specific item.

    Works with:
      - Strings (substring check)
      - Lists, tuples, sets (membership check)

    Example:
        Field("tags").contains("vip")
        Field("name").contains("admin")
    """

    field_name: str
    """Name of the field to check for containment."""

    value: Any
    """The value to look for inside the field."""

    def evaluate(self, data: Any) -> bool:
        """Evaluate whether the field contains the specified value.

        Returns:
            True if the value is found in the field, False otherwise (including
            when the field is missing or not a container).
        """

        collection = get_nested(data, self.field_name)
        if collection is None:
            return False
        try:
            return self.value in collection
        except TypeError:
            return False

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the rule to a dictionary."""

        return {"type": self._type, "field": self.field_name, "value": self.value}

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> "ContainsRule":
        """Deserialize from dictionary representation."""

        return cls(field_name=data["field"], value=data["value"])

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.field_name == other.field_name and self.value == other.value

    def __repr__(self) -> str:
        """Return a readable representation showing Field.contains() syntax."""

        return f"Field({self.field_name!r}).contains({self.value!r})"
