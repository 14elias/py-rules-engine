import re
from .base import Predicate

@Predicate.register("regex")
class Regex(Predicate):
    def __init__(self, pattern: str):
        self.pattern = pattern

        try:
            re.compile(pattern)
        except re.error as e:
            raise e from None

    def evaluate(self, value):
        if not isinstance(value, str):
            return False
        
        try:
            return re.search(self.pattern, value) is not None
        except re.error:
            return False

    def to_dict(self):
        return {
            "type": self._type,
            "pattern": self.pattern
        }

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["pattern"])


    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.pattern == other.pattern
    


@Predicate.register("startswith")
class StartsWith(Predicate):
    def __init__(self, prefix):
        self.prefix = prefix

    def evaluate(self, value):
        if not isinstance(value, str):
            return False
        
        if not isinstance(self.prefix, str):    # optional: be strict
            return False
        
        return value.startswith(self.prefix)

    def to_dict(self):
        return {"type": self._type, "prefix": self.prefix}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["prefix"])


    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.prefix == other.prefix
    


@Predicate.register("endswith")
class EndsWith(Predicate):
    def __init__(self, suffix):
        self.suffix = suffix

    def evaluate(self, value):
        if not isinstance(value, str):
            return False
        
        if not isinstance(self.suffix, str):    # optional: be strict
            return False
        
        return value.endswith(self.suffix)

    def to_dict(self):
        return {"type": self._type, "suffix": self.suffix}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["suffix"])
    

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.suffix == other.suffix