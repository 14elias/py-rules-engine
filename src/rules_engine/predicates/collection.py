from .base import Predicate

@Predicate.register("contains")
class Contains(Predicate):
    def __init__(self, item):
        self.item = item

    def evaluate(self, value):
        return self.item in value

    def to_dict(self):
        return {
            "type": self._type,
            "item": self.item
        }

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["item"])
    


@Predicate.register("in")
class In(Predicate):
    def __init__(self, options):
        self.options = options

    def evaluate(self, value):
        return value in self.options

    def to_dict(self):
        return {"type": self._type, "options": self.options}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["options"])
    


@Predicate.register("len_eq")
class LengthEquals(Predicate):
    def __init__(self, length):
        self.length = length

    def evaluate(self, value):
        return len(value) == self.length

    def to_dict(self):
        return {"type": self._type, "length": self.length}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["length"])
    


@Predicate.register("len_gt")
class LengthGreaterThan(Predicate):
    def __init__(self, length):
        self.length = length

    def evaluate(self, value):
        return len(value) > self.length

    def to_dict(self):
        return {"type": self._type, "length": self.length}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["length"])



@Predicate.register("len_lt")
class LengthLessThan(Predicate):
    def __init__(self, length):
        self.length = length

    def evaluate(self, value):
        return len(value) < self.length

    def to_dict(self):
        return {"type": self._type, "length": self.length}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["length"])