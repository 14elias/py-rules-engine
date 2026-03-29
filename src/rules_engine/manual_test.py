# if __name__ == "__main__":
#     # Create complex rule
#     import json
#     from rules_engine.core.base import Rule
#     from rules_engine import Field
#     rule = (
#         ((Field("age") >= 18) & (Field("country") == "US")) |
#         (Field("is_verified") == True)
#     )

#     print("Original Rule:", rule)

#     # Serialize
#     data_dict = rule.to_dict()
#     json_str = rule.to_json()

#     print("\nSerialized Dict:", json.dumps(data_dict, indent=2))
#     print("\nSerialized JSON:", json_str)

#     # Deserialize
#     loaded_rule = Rule.from_dict(data_dict)
#     loaded_from_json = Rule.from_json(json_str)

#     # Test
#     test_data = {"age": 25, "country": "ET", "is_verified": True}
#     print("\nEvaluation after round-trip:", loaded_rule.evaluate(test_data))


#     print(f'classes that are registerd: {Rule._registry}')



    """🚀 Recommendation for PyPI
To be truly "Production Ready" for PyPI, I recommend:

Code Coverage: Run pytest --cov=src and ensure you are at >95%.

Linting/Typing: Run mypy on your code. Since you use from __future__ import annotations, ensuring types are correct is vital for library users.

Docstrings: Ensure every Rule class has a short docstring explaining what it does.

CI/CD: Set up a GitHub Action to run these tests on every push."""