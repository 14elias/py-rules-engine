from .base import Predicate


@Predicate.register("and")
class And(Predicate):
    def __init__(self, *predicates):
        self.predicates = predicates

    def evaluate(self, value):
        return all(p.evaluate(value) for p in self.predicates)

    def to_dict(self):
        return {
            "type": self._type,
            "predicates": [p.to_dict() for p in self.predicates]
        }

    @classmethod
    def _from_dict_impl(cls, data):
        from rules_engine.predicates.base import Predicate
        return cls(*[Predicate.from_dict(p) for p in data["predicates"]])
    


@Predicate.register("or")
class Or(Predicate):
    def __init__(self, *predicates):
        self.predicates = predicates

    def evaluate(self, value):
        return any(p.evaluate(value) for p in self.predicates)

    def to_dict(self):
        return {
            "type": self._type,
            "predicates": [p.to_dict() for p in self.predicates]
        }

    @classmethod
    def _from_dict_impl(cls, data):
        from rules_engine.predicates.base import Predicate
        return cls(*[Predicate.from_dict(p) for p in data["predicates"]])
    



@Predicate.register("not")
class Not(Predicate):
    def __init__(self, predicate):
        self.predicate = predicate

    def evaluate(self, value):
        return not self.predicate.evaluate(value)

    def to_dict(self):
        return {
            "type": self._type,
            "predicate": self.predicate.to_dict()
        }

    @classmethod
    def _from_dict_impl(cls, data):
        from rules_engine.predicates.base import Predicate
        return cls(Predicate.from_dict(data["predicate"]))