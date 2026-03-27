from .base import Predicate

@Predicate.register("equals")
class Equals(Predicate):
    def __init__(self, expected):
        self.expected = expected

    def evaluate(self, value):
        return value == self.expected

    def to_dict(self):
        return {
            "type": self._type,
            "expected": self.expected
        }

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["expected"])



@Predicate.register("not_equals")
class NotEquals(Predicate):
    def __init__(self, expected):
        self.expected = expected

    def evaluate(self, value):
        return value != self.expected

    def to_dict(self):
        return {"type": self._type, "expected": self.expected}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["expected"])



@Predicate.register("gt")
class GreaterThan(Predicate):
    def __init__(self, threshold):
        self.threshold = threshold

    def evaluate(self, value):
        return value > self.threshold

    def to_dict(self):
        return {"type": self._type, "threshold": self.threshold}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["threshold"])



@Predicate.register("gte")
class GreaterThanOrEqual(Predicate):
    def __init__(self, threshold):
        self.threshold = threshold

    def evaluate(self, value):
        return value >= self.threshold

    def to_dict(self):
        return {"type": self._type, "threshold": self.threshold}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["threshold"])


@Predicate.register("lt")
class LessThan(Predicate):
    def __init__(self, threshold):
        self.threshold = threshold

    def evaluate(self, value):
        return value < self.threshold

    def to_dict(self):
        return {"type": self._type, "threshold": self.threshold}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["threshold"])
    


@Predicate.register("lte")
class LessThanOrEqual(Predicate):
    def __init__(self, threshold):
        self.threshold = threshold

    def evaluate(self, value):
        return value <= self.threshold

    def to_dict(self):
        return {"type": self._type, "threshold": self.threshold}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["threshold"])
