import pytest

@pytest.fixture
def sample_data():
    return {
        "age": 25,
        "country": "US",
        "name": "Abel",
        "tags": ["python", "ai"],
        "scores": [10, 20, 30],
        "profile": {
            "email": "test@example.com"
        }
    }