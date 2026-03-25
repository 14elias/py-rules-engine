if __name__ == "__main__":
    # Create complex rule
    import json
    from rules_engine.core.base import Rule
    from rules_engine.field.field import Field
    rule = (
        ((Field("age") >= 18) & (Field("country") == "US")) |
        (Field("is_verified") == True)
    )

    print("Original Rule:", rule)

    # Serialize
    data_dict = rule.to_dict()
    json_str = rule.to_json()

    print("\nSerialized Dict:", json.dumps(data_dict, indent=2))
    print("\nSerialized JSON:", json_str)

    # Deserialize
    loaded_rule = Rule.from_dict(data_dict)
    loaded_from_json = Rule.from_json(json_str)

    # Test
    test_data = {"age": 25, "country": "ET", "is_verified": True}
    print("\nEvaluation after round-trip:", loaded_rule.evaluate(test_data))