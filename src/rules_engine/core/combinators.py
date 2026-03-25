from dataclasses import dataclass
from typing import Any, Dict
from .base import Rule

@Rule.register
@dataclass(frozen=True)
class AndRule(Rule):
    left: Rule
    right: Rule

    def evaluate(self, data: Any) -> bool:
        return self.left.evaluate(data) and self.right.evaluate(data)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "AndRule",
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
        }

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(
            Rule.from_dict(data["left"]),
            Rule.from_dict(data["right"]),
        )


@Rule.register
@dataclass(frozen=True)
class OrRule(Rule):
    left: Rule
    right: Rule

    def evaluate(self, data: Any) -> bool:
        return self.left.evaluate(data) or self.right.evaluate(data)

    def to_dict(self):
        return {
            "type": "OrRule",
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
        }

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(
            Rule.from_dict(data["left"]),
            Rule.from_dict(data["right"]),
        )


@Rule.register
@dataclass(frozen=True)
class NotRule(Rule):
    child: Rule

    def evaluate(self, data):
        return not self.child.evaluate(data)

    def to_dict(self):
        return {"type": "NotRule", "child": self.child.to_dict()}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(Rule.from_dict(data["child"]))