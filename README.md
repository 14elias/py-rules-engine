# rules-engine

Composable, elegant business rules engine for Python using operator overloading and expression trees.

Write rules like:

````python
from rules_engine import Field

rule = (Field("age") >= 18) & (Field("is_premium") == True) | (Field("role") == "admin")
print(rule({"age": 25, "is_premium": False, "role": "user"}))  # True

### Nested Fields (Dot Notation)

You can access nested dictionary keys using dot notation:

```python
from simplerules import Field

# Example data
user = {
    "profile": {
        "age": 25,
        "country": "ET"
    },
    "roles": ["user", "editor"]
}

# Rules
age_ok      = Field("profile.age") >= 18
in_ethiopia = Field("profile.country") == "ET"
has_role    = Field("roles").contains("editor")

print((age_ok & in_ethiopia).evaluate(user))     # True



#### New predicates section

```markdown
### Rich Predicates & Collection Checks

`Field` objects support method-style predicates for strings, lists, sets, etc.

```python
# Collection checks
has_vip     = Field("tags").contains("vip")
many_orders = Field("orders").len() >= 10
has_premium = Field("plans").any(lambda p: "premium" in p)
all_admins  = Field("roles").all() == "admin"           # every item equals "admin"
is_staff    = Field("roles").all(lambda r: r in {"admin", "staff"})

# String checks
corporate   = Field("email").matches(r".+@company\.com$")
guest_user  = Field("username").startswith("guest_")

# Combining
power_user = has_premium & (many_orders | has_vip)
````
