from dataclasses import dataclass
from typing import Any, Dict
from .base import Rule

@Rule.register("AndRule")
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
            "type": self._type,
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
        }

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(
            Rule.from_dict(data["left"]),
            Rule.from_dict(data["right"]),
        )
    

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return (
            self.left == other.left and
            self.right == other.right
        )


@Rule.register("OrRule")
@dataclass(frozen=True)
class OrRule(Rule):
    left: Rule
    right: Rule

    def evaluate(self, data: Any) -> bool:
        if self.left.evaluate(data):
            return True
        return self.right.evaluate(data)

    def to_dict(self):
        return {
            "type": self._type,
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
        }

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(
            Rule.from_dict(data["left"]),
            Rule.from_dict(data["right"]),
        )
    

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return (
            self.left == other.left and
            self.right == other.right
        )


@Rule.register("NotRule")
@dataclass(frozen=True)
class NotRule(Rule):
    child: Rule

    def evaluate(self, data):
        return not self.child.evaluate(data)

    def to_dict(self):
        return {"type": self._type, "child": self.child.to_dict()}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(Rule.from_dict(data["child"]))
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return self.child == other.child
    

@Rule.register("ParenRule")
@dataclass(frozen=True)
class ParenRule(Rule):
    child: Rule

    def evaluate(self, data: Any) -> bool:
        return self.child.evaluate(data)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self._type,
            "child": self.child.to_dict(),
        }

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> 'ParenRule':
        return cls(child=Rule.from_dict(data["child"]))
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return self.child == other.child

    def __repr__(self) -> str:
        return f"({self.child!r})"