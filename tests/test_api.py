from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_api_clean_ok():
    payload = {"Name": "Bauer, Sir. John", "Age": 30, "Pclass": 3, "Fare": 8.05}
    r = client.post("/clean/passenger", json=payload)

    assert r.status_code == 200
    assert r.json() == {
        "Name": "Bauer, Sir. John", "Age": 30, "Pclass": 3,
        "Fare": 8.05, "Title": "Sir", "Title_Normalized": "Mr"
    }

def test_api_missing_field():
    payload = {"Name": "Bauer, Sir. John", "Fare": 5.0}
    r = client.post("/clean/passenger", json=payload)
    assert r.status_code == 422
    error_types = [error["msg"] for error in r.json()["detail"]]
    assert error_types == [
        "Field required",
        "Field required"
    ]

def test_api_invalid_value():
    payload = {"Name": "John", "Age": -10, "Pclass": 5, "Fare": 0}
    r = client.post("/clean/passenger", json=payload)
    # FastAPI + Pydantic perform model parsing and validation automatically and
    # will return 422 Unprocessable Entity for model/schema validation errors.
    assert r.status_code == 422
    error_types = [error["msg"] for error in r.json()["detail"]]
    assert error_types == [
        "Value error, age must >=0",
        "Value error, Pclass must be 1, 2, or 3",
        "Value error, Fare must be positive"
    ]

def test_api_invalid_type():
    payload = {"Name": "Invalid", "Age": 10, "Pclass": "first", "Fare": 21.0}
    r = client.post("/clean/passenger", json=payload)
    assert r.status_code == 422
    error_types = [error["msg"] for error in r.json()["detail"]]
    assert error_types == [
        'Value error, Pclass must be 1, 2, or 3'
    ]


