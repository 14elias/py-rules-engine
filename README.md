# rules-engine

A composable rule engine for Python that lets you build reusable, JSON-serializable logic using a clean, expressive syntax.

## Example

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

## Features

* Compose rules using `&` (AND), `|` (OR), and `~` (NOT)
* Safe nested field access using dot notation
* JSON serialization / deserialization
* Built-in predicates (contains, regex, prefix, length)
* Clean DSL for building complex logic

---

## Nested Fields

Access deeply nested data using dot notation:

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

## Predicates

### Collections

```python
has_vip     = Field("tags").contains("vip")
many_orders = Field("orders").len() >= 10
```

### Strings

```python
corporate  = Field("email").matches(r".+@company\.com$")
guest_user = Field("username").startswith("guest_")
```

---

## Serialization

```python
rule = (Field("age") >= 18)

json_str = rule.to_json()
restored = Rule.from_json(json_str)
```

---

## Use Cases

* API request validation
* Feature flags and access control
* Filtering pipelines
* Rule-based AI decision systems
* Fraud detection / business logic engines

---

## Notes

* `AnyRule` / `AllRule` with custom lambda predicates are not serializable.
* Use parentheses `()` to control logical precedence explicitly.

---

## Contributing

Contributions are welcome. Feel free to open issues or submit pull requests.

---
