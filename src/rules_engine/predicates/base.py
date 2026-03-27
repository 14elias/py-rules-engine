from typing import Any, Dict, Type

class Predicate:
    _registry: Dict[str, Type["Predicate"]] = {}

    def evaluate(self, value: Any) -> bool:
        raise NotImplementedError

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Predicate":
        if not isinstance(data, dict) or "type" not in data:
            raise ValueError("Predicate must have a 'type' field")

        pred_type = data["type"]

        if pred_type not in cls._registry:
            raise ValueError(f"Unknown predicate type: {pred_type}")

        return cls._registry[pred_type]._from_dict_impl(data)

    @classmethod
    def register(cls, name: str):
        def decorator(subclass):
            cls._registry[name] = subclass
            subclass._type = name
            return subclass
        return decorator