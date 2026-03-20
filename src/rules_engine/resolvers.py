from dataclasses import dataclass
from .core import Rule


@dataclass(frozen=True)
class ParenRule(Rule):
    child: Rule
    
    def evaluate(self, data):
        return self.child.evaluate(data)
    
    def __repr__(self):
        return f"({self.child!r})"
    


def P(rule: Rule) -> Rule:
    return ParenRule(rule)


