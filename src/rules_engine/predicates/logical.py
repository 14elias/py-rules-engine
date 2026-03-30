from .base import Predicate


@Predicate.register("and")
class And(Predicate):
    """Logical AND predicate that requires ALL child predicates to be True."""

    def __init__(self, *predicates):
        if not predicates:
            self.predicates = ()
            return  # allow empty And (vacuous truth)

        for i, p in enumerate(predicates):
            if not isinstance(p, Predicate):
                raise TypeError(
                    f"All arguments to And() must be Predicate instances. "
                    f"Got {type(p).__name__} at position {i}."
                )

        self.predicates = predicates

    def evaluate(self, value):
        return all(p.evaluate(value) for p in self.predicates)

    def to_dict(self):
        return {
            "type": self._type,
            "predicates": [p.to_dict() for p in self.predicates],
        }

    @classmethod
    def _from_dict_impl(cls, data):
        from rules_engine.predicates.base import Predicate

        return cls(*[Predicate.from_dict(p) for p in data["predicates"]])

    def __eq__(self, other: object) -> bool:
        # 1. Check if the 'other' object is even the same type
        if not isinstance(other, self.__class__):
            return False

        # 2. Check if they have the same number of child predicates
        if len(self.predicates) != len(other.predicates):
            return False

        # 3. Compare each child predicate in order
        # This relies on each child predicate (e.g., Comparison)
        # also having its own __eq__ implemented.
        return all(p1 == p2 for p1, p2 in zip(self.predicates, other.predicates))


@Predicate.register("or")
class Or(Predicate):
    """Logical OR predicate that returns True if ANY child predicate is True."""

    def __init__(self, *predicates):
        if not predicates:
            self.predicates = ()
            return  # allow empty Or (vacuous falsity)

        for i, p in enumerate(predicates):
            if not isinstance(p, Predicate):
                raise TypeError(
                    f"All arguments to Or() must be Predicate instances. "
                    f"Got {type(p).__name__} at position {i}."
                )

        self.predicates = predicates

    def evaluate(self, value):
        return any(p.evaluate(value) for p in self.predicates)

    def to_dict(self):
        return {
            "type": self._type,
            "predicates": [p.to_dict() for p in self.predicates],
        }

    @classmethod
    def _from_dict_impl(cls, data):
        from rules_engine.predicates.base import Predicate

        return cls(*[Predicate.from_dict(p) for p in data["predicates"]])

    def __eq__(self, other: object) -> bool:
        # 1. Check if the 'other' object is even the same type
        if not isinstance(other, self.__class__):
            return False

        # 2. Check if they have the same number of child predicates
        if len(self.predicates) != len(other.predicates):
            return False

        # 3. Compare each child predicate in order
        # This relies on each child predicate (e.g., Comparison)
        # also having its own __eq__ implemented.
        return all(p1 == p2 for p1, p2 in zip(self.predicates, other.predicates))


@Predicate.register("not")
class Not(Predicate):
    """Logical NOT predicate that inverts the result of a child predicate."""

    def __init__(self, predicate):
        if not isinstance(predicate, Predicate):
            raise TypeError(
                f"Argument to Not() must be a Predicate instance. "
                f"Got {type(predicate).__name__} instead."
            )
        self.predicate = predicate

    def evaluate(self, value):
        return not self.predicate.evaluate(value)

    def to_dict(self):
        return {"type": self._type, "predicate": self.predicate.to_dict()}

    @classmethod
    def _from_dict_impl(cls, data):
        from rules_engine.predicates.base import Predicate

        return cls(Predicate.from_dict(data["predicate"]))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.predicate == other.predicate
