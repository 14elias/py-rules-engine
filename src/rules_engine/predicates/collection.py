from .base import Predicate


@Predicate.register("contains")
class Contains(Predicate):
    """Predicate that checks if a value contains a specific item (membership test)."""

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
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return self.item == other.item


@Predicate.register("in")
class In(Predicate):
    """Predicate that checks if a value is present in a given set of options."""

    def __init__(self, options):
        self.options = options

    def evaluate(self, value):
        return value in self.options

    def to_dict(self):
        return {"type": self._type, "options": self.options}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["options"])
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return self.options == other.options
    


@Predicate.register("len_eq")
class LengthEquals(Predicate):
    """Predicate that checks if the length of a value equals a specific number."""

    def __init__(self, length):
        self.length = length

    def evaluate(self, value):
        return len(value) == self.length

    def to_dict(self):
        return {"type": self._type, "length": self.length}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["length"])
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return self.length == other.length
    


@Predicate.register("len_gt")
class LengthGreaterThan(Predicate):
    """Predicate that checks if the length of a value is greater than a number."""

    def __init__(self, length):
        self.length = length

    def evaluate(self, value):
        return len(value) > self.length

    def to_dict(self):
        return {"type": self._type, "length": self.length}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["length"])
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return self.length == other.length



@Predicate.register("len_lt")
class LengthLessThan(Predicate):
    """Predicate that checks if the length of a value is less than a number."""
    
    def __init__(self, length):
        self.length = length

    def evaluate(self, value):
        return len(value) < self.length

    def to_dict(self):
        return {"type": self._type, "length": self.length}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls(data["length"])
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return self.length == other.length