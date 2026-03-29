from .base import Predicate

@Predicate.register("equals")
class Equals(Predicate):
    def __init__(self, expected):
        self.expected = expected

    def evaluate(self, value):
        if type(value) != type(self.expected):
            return False
        return value == self.expected

    def to_dict(self):
        return {
            "type": self._type,
            "expected": self.expected
        }

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["expected"])
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return self.expected == other.expected



@Predicate.register("not_equals")
class NotEquals(Predicate):
    def __init__(self, expected):
        self.expected = expected

    def evaluate(self, value):
        if type(value) != type(self.expected):
            return True
        
        return value != self.expected

    def to_dict(self):
        return {"type": self._type, "expected": self.expected}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["expected"])

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return self.expected == other.expected


@Predicate.register("gt")
class GreaterThan(Predicate):
    def __init__(self, threshold):
        self.threshold = threshold

    def evaluate(self, value):
        if type(value) != type(self.threshold):
            return False
        return value > self.threshold

    def to_dict(self):
        return {"type": self._type, "threshold": self.threshold}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["threshold"])
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return self.threshold == other.threshold



@Predicate.register("gte")
class GreaterThanOrEqual(Predicate):
    def __init__(self, threshold):
        self.threshold = threshold

    def evaluate(self, value):
        if type(value) != type(self.threshold):
            return False
        return value >= self.threshold

    def to_dict(self):
        return {"type": self._type, "threshold": self.threshold}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["threshold"])
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return self.threshold == other.threshold


@Predicate.register("lt")
class LessThan(Predicate):
    def __init__(self, threshold):
        self.threshold = threshold

    def evaluate(self, value):
        if type(value) != type(self.threshold):
            return False
        return value < self.threshold

    def to_dict(self):
        return {"type": self._type, "threshold": self.threshold}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["threshold"])
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return self.threshold == other.threshold
    


@Predicate.register("lte")
class LessThanOrEqual(Predicate):
    def __init__(self, threshold):
        self.threshold = threshold

    def evaluate(self, value):
        if type(value) != type(self.threshold):
            return False
        return value <= self.threshold

    def to_dict(self):
        return {"type": self._type, "threshold": self.threshold}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["threshold"])
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return self.threshold == other.threshold
