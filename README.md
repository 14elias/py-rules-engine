# rules-engine-py

![CI](https://github.com/14elias/rules-engine/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/github/license/14elias/py-rules-engine)
![Version](https://img.shields.io/github/v/release/14elias/py-rules-engine)

**A composable, JSON-serializable rule engine for Python.**

Build reusable, expressive business logic using a clean and intuitive DSL. Perfect for API validation, feature flags, access control, data filtering, fraud detection, and rule-based decision systems.

---

## ✨ Features

- Elegant DSL using `Field("path")` with natural Python operators (`>=`, `==`, `&`, `|`, `~`)
- Deep nested field access (`"user.profile.age"`, `"items.0.price"`)
- Full JSON serialization & deserialization support
- Powerful collection operations: `.any()` and `.all()`
- Rich string, numeric, and length-based rules
- Logical composition with `&` (AND), `|` (OR), and `~` (NOT)
- Extensible via custom predicates
- Zero runtime dependencies

---

## 🚀 Quick Start

### Installation

```bash
pip install rules-engine-py
```

### Simple Example

```python
from rules_engine import Field

# Build expressive rules using Field
rule = (
    (Field("age") >= 18) & (Field("is_premium") == True)
) | (Field("role") == "admin")

data = {"age": 25, "is_premium": False, "role": "user"}

print(rule.evaluate(data))   # True
```

### Working with Nested Data

```python
user = {
    "profile": {"age": 25, "country": "ET"},
    "roles": ["user", "editor"],
    "bio": "Hello world from Ethiopia"
}

age_ok = Field("profile.age") >= 18
from_ethiopia = Field("profile.country") == "ET"
has_editor = Field("roles").contains("editor")
long_bio = Field("bio").len() > 10

rule = (age_ok & from_ethiopia) | (has_editor & long_bio)

print(rule.evaluate(user))   # True
```

---

## 🧠 Core Concepts

### Field — The Main DSL Builder

Field is the primary way to create rules. It uses Python's operator overloading and method chaining to create readable rules.

```python
from rules_engine import Field

# Simple comparisons
Field("age") >= 18
Field("status") == "active"

# String operations
Field("name").startswith("guest")
Field("email").matches(r".+@company\.com")

# Collection operations
Field("tags").contains("python")
Field("tags").len() >= 3
```

### Supported Operations on Field

| Operation              | Example                                       | Description                  |
| ---------------------- | --------------------------------------------- | ---------------------------- |
| `==, !=, >, >=, <, <=` | `Field("age") >= 18`                          | Numeric / value comparison   |
| `.startswith()`        | `Field("name").startswith("Ab")`              | String prefix                |
| `.endswith()`          | `Field("email").endswith(".com")`             | String suffix                |
| `.matches()`           | `Field("email").matches(r".+@example\\.com")` | Regex match                  |
| `.contains()`          | `Field("tags").contains("python")`            | Check if value contains item |
| `.len()`               | `Field("tags").len() >= 3`                    | Length comparison            |
| `.any(predicate)`      | `Field("scores").any(GreaterThan(50))`        | Any item matches predicate   |
| `.all(predicate)`      | `Field("tags").all(StartsWith("py"))`         | All items match predicate    |

---

### Logical Composition

You can combine rules using Python operators:

```python
from rules_engine import Field

adult = Field("age") >= 18
premium = Field("is_premium") == True
admin = Field("role") == "admin"

# Combine rules
main_rule = (adult & premium) | admin

# Negation
not_admin = ~admin
```

---

## 🔍 Predicates

Predicates are used primarily with `.any()` and `.all()` on collections.

### Built-in Predicates

```python
from rules_engine.predicates import (
    Equals, NotEquals,
    GreaterThan, GreaterThanOrEqual,
    LessThan, LessThanOrEqual,
    StartsWith, EndsWith, Regex,
    Contains, And, Or, Not
)
```

### Examples

```python
from rules_engine.predicates import Contains, GreaterThan, Equals

data = {
    "tags": ["python", "ai", "ethiopia"],
    "scores": [10, 20, 35]
}

has_ai_tag = Field("tags").any(Contains("ai"))
has_high_score = Field("scores").any(GreaterThan(30))
has_exact_two = Field("scores").any(Equals(2))
```

You can also combine predicates logically:

```python
complex_pred = And(StartsWith("py"), EndsWith("on"))
rule = Field("tags").any(complex_pred)
```

---

## 💾 Serialization

All rules are fully serializable to JSON and can be restored later.

```python
from rules_engine import Field, Rule

rule = (Field("age") >= 18) & Field("country") == "ET"

# Save to JSON
json_str = rule.to_json()

# Load from JSON
restored = Rule.from_json(json_str)

# Both rules behave identically
assert rule.evaluate(data) == restored.evaluate(data)
```

---

## ⚙️ Creating Custom Predicates

Custom predicates can be created by subclassing `Predicate` and registering them:

```python
from rules_engine.predicates.base import Predicate

@Predicate.register("is_even")
class IsEven(Predicate):
    def evaluate(self, value):
        if not isinstance(value, (int, float)):
            return False
        return value % 2 == 0

    def to_dict(self):
        return {"type": self._type}

    @classmethod
    def _from_dict_impl(cls, data):
        return cls()

    def __eq__(self, other):
        return isinstance(other, IsEven)
```

Then use it:

```python
rule = Field("score").any(IsEven())
```

> Note: Custom Rules are currently not directly supported via the DSL. All rules must be created through the Field class.

---

## 📚 API Reference

### Main Imports

```python
from rules_engine import Field, Rule
from rules_engine.predicates import (
    Equals, NotEquals, GreaterThan, GreaterThanOrEqual,
    LessThan, LessThanOrEqual, StartsWith, EndsWith, Regex,
    Contains, And, Or, Not
)
```

### Key Classes

- **Field** — DSL entry point for building rules
- **Rule** — Base class for all rules (used mainly for deserialization)
- **Predicate** — Base class for predicates used in `.any()` / `.all()`

---

## 🧩 Use Cases

- API request validation
- Feature flags and access control
- Dynamic data filtering
- Fraud detection systems
- Rule-based decision engines
- User segmentation and personalization

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome!
See CONTRIBUTING.md for guidelines.

---

## 📄 License

MIT License
