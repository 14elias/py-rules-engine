import pytest

@pytest.fixture
def sample_data2():
    return {
        "age": 25,
        "country": "US",
        "name": "Abel",
        "tags": ["python", "ai", "ethiopia"],
        "scores": [10, 20, 30],
        "profile": {
            "email": "test@example.com",
            "hobbies": ["reading", "coding"],
            "empty_list": [],
            "none_value": None,
        },
        "bio": "Hello world",
        "empty_string": "",
        "single_tuple": (1, 2, 3),
        "nested_dict": {"key": "value"},
    }