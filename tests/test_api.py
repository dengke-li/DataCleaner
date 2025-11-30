from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_api_clean_ok():
    payload = {"Name": "Bauer, Sir. John", "Age": 30, "Pclass": 3, "Fare": 8.05}
    r = client.post("/clean/passenger", json=payload)

    assert r.status_code == 200
    assert r.json() == {
        "Name": "Bauer, Sir. John",
        "Age": 30,
        "Pclass": 3,
        "Fare": 8.05,
        "Title": "Sir",
        "Title_Normalized": "Mr",
    }


def test_api_missing_field():
    payload = {"Name": "Bauer, Sir. John", "Fare": 5.0}
    r = client.post("/clean/passenger", json=payload)
    assert r.status_code == 422
    assert r.json() == {
        "error": "Schema Validation error",
        "detail": [
            {
                "loc": ["body", "Age"],
                "msg": "Field required",
                "input": {"Name": "Bauer, Sir. John", "Fare": 5.0},
            },
            {
                "loc": ["body", "Pclass"],
                "msg": "Field required",
                "input": {"Name": "Bauer, Sir. John", "Fare": 5.0},
            },
        ],
    }


def test_api_invalid_value():
    payload = {"Name": "John", "Age": -10, "Pclass": 5, "Fare": 0}
    r = client.post("/clean/passenger", json=payload)
    # FastAPI + Pydantic perform model parsing and validation automatically and
    # will return 422 Unprocessable Entity for model/schema validation errors.
    assert r.status_code == 422
    error_types = [error["msg"] for error in r.json()["detail"]]
    assert r.json() == {
        "error": "Schema Validation error",
        "detail": [
            {"loc": ["body", "Age"], "msg": "Value error, age must >=0", "input": -10},
            {
                "loc": ["body", "Pclass"],
                "msg": "Value error, Pclass must be 1, 2, or 3",
                "input": 5,
            },
            {
                "loc": ["body", "Fare"],
                "msg": "Value error, Fare must be positive",
                "input": 0,
            },
        ],
    }


def test_api_invalid_type():
    payload = {"Name": "Invalid", "Age": 10, "Pclass": "first", "Fare": 21.0}
    r = client.post("/clean/passenger", json=payload)
    assert r.status_code == 422
    print(r.json())
    assert r.json() == {
        "error": "Schema Validation error",
        "detail": [
            {
                "loc": ["body", "Pclass"],
                "msg": "Value error, Pclass must be 1, 2, or 3",
                "input": "first",
            }
        ],
    }


def test_api_empty_field():
    payload = {"Name": None, "Age": 44, "Pclass": 1, "Fare": 15.5}
    r = client.post("/clean/passenger", json=payload)
    assert r.status_code == 422
    print(r.json())
    assert r.json() == {
        "error": "Schema Validation error",
        "detail": [
            {
                "loc": ["body", "Name"],
                "msg": "Value error, Name must not be blank",
                "input": None,
            }
        ],
    }


def test_api_invalid_json():
    payload = "invalid json"
    r = client.post("/clean/passenger", json=payload)
    assert r.status_code == 400

    assert r.json() == {
        "error": "Invalid JSON body",
        "detail": [
            {
                "type": "model_attributes_type",
                "loc": ["body"],
                "msg": "Input should be a valid dictionary or object to extract fields from",
                "input": "invalid json",
            }
        ],
    }
