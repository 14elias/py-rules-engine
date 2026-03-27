import re
from .base import Predicate

@Predicate.register("regex")
class Regex(Predicate):
    def __init__(self, pattern: str):
        self.pattern = pattern

    def evaluate(self, value):
        return re.match(self.pattern, value) is not None

    def to_dict(self):
        return {
            "type": self._type,
            "pattern": self.pattern
        }

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["pattern"])
    


@Predicate.register("startswith")
class StartsWith(Predicate):
    def __init__(self, prefix):
        self.prefix = prefix

    def evaluate(self, value):
        return value.startswith(self.prefix)

    def to_dict(self):
        return {"type": self._type, "prefix": self.prefix}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["prefix"])
    


@Predicate.register("endswith")
class EndsWith(Predicate):
    def __init__(self, suffix):
        self.suffix = suffix

    def evaluate(self, value):
        return value.endswith(self.suffix)

    def to_dict(self):
        return {"type": self._type, "suffix": self.suffix}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["suffix"])