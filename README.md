# rules-engine

A composable, JSON-serializable rule engine for Python.

Build reusable, expressive logic using a clean DSL — perfect for validation, filtering, and decision systems.

---

## ✨ Installation

```bash
pip install rules-engine
```

---

## 🚀 Quick Example

```python
from rules_engine import Field

rule = (
    ((Field("age") >= 18) & (Field("is_premium") == True)) |
    (Field("role") == "admin")
)

data = {"age": 25, "is_premium": False, "role": "user"}

print(rule.evaluate(data))  # True
```

---

## 🔥 Features

- Compose rules using:
  - `&` → AND
  - `|` → OR
  - `~` → NOT

- Safe nested field access using dot notation
- JSON serialization / deserialization
- Built-in predicates:
  - `contains`
  - `regex / matches`
  - `startswith`
  - `length`

- Clean and expressive DSL
- Extensible architecture (custom rules & predicates)

---

## 🧩 Nested Fields

Access deeply nested data easily:

```python
user = {
    "profile": {
        "age": 25,
        "country": "ET"
    },
    "roles": ["user", "editor"]
}

age_ok      = Field("profile.age") >= 18
in_ethiopia = Field("profile.country") == "ET"
has_role    = Field("roles").contains("editor")

print((age_ok & in_ethiopia).evaluate(user))  # True
```

---

## 🧠 Predicates

### Collections

```python
Field("tags").contains("vip")
Field("orders").len() >= 10
```

### Strings

```python
Field("email").matches(r".+@company\.com$")
Field("username").startswith("guest_")
```

---

## 🔄 Serialization

```python
from rules_engine import Field, Rule

rule = Field("age") >= 18

json_str = rule.to_json()
restored = Rule.from_json(json_str)

assert rule.evaluate({"age": 20}) == restored.evaluate({"age": 20})
```

---

## 🧪 Example Use Cases

- API request validation
- Feature flags & access control
- Data filtering pipelines
- Rule-based AI decision systems
- Fraud detection systems

## 🏗️ Project Structure (for contributors)

```
src/
  rules_engine/
    core/
    rules/
    predicates/
    field/
    utils/
```

---

## 🤝 Contributing

Contributions are welcome!

- Open an issue for bugs or feature requests
- Submit pull requests for improvements
- Help expand predicates and rule types

---

## 📄 License

MIT License © 2026 Elias
