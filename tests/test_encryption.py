import base64
import json
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def toBase64(s):
    s = json.dumps(s).encode("utf-8")
    return base64.b64encode(s).decode("utf-8")


def test_encryption_no_payload():
    response = client.post("/encrypt")
    assert response.status_code == 422


def test_encryption_empty_payload():
    response = client.post("/encrypt", json={})
    assert response.status_code == 200
    assert response.json() == {}


def test_encryption_not_json():
    response = client.post("/encrypt", content="Not a JSON")
    assert response.status_code == 422


def test_encryption_1_attribute():
    payload = {"name":"John Doe"}
    response = client.post("/encrypt", json=payload)
    assert response.status_code == 200
    encrypted_data = response.json().get("name")
    assert encrypted_data == toBase64("John Doe")


def test_encryption_2_attributes():
    payload = {"name":"John Doe", "age":30}
    response = client.post("/encrypt", json=payload)
    assert response.status_code == 200
    encrypted_data = response.json()
    assert encrypted_data.get("name") == toBase64("John Doe")
    assert encrypted_data.get("age") == toBase64(30)


def test_encryption_null_value():
    payload = {"name": None}
    response = client.post("/encrypt", json=payload)
    assert response.status_code == 200
    encrypted_data = response.json().get("name")
    assert encrypted_data == toBase64(None)


def test_encryption_boolean_value():
    payload = {"alive": True}
    response = client.post("/encrypt", json=payload)
    assert response.status_code == 200
    encrypted_data = response.json().get("alive")
    assert encrypted_data == toBase64(True)


def test_encryption_list_value():
    payload = {"numbers": [1, 2, 3]}
    response = client.post("/encrypt", json=payload)
    assert response.status_code == 200
    encrypted_data = response.json().get("numbers")
    expected = toBase64(payload["numbers"])
    assert encrypted_data == expected


def test_encryption_only_first_depth():
    payload = {
        "contact": {
            "email": "john@example.com",
            "phone": "123-456-7890"
        }
    }
    response = client.post("/encrypt", json=payload)
    assert response.status_code == 200
    encrypted_data = response.json().get("contact")
    expected = toBase64(payload["contact"])
    assert encrypted_data == expected


def test_encryption_maintains_order():
    payload = {
        "name": "John Doe",
        "age": 30,
        "contact": {
            "email": "john@example.com",
            "phone": "123-456-7890"
        }
    }
    response = client.post("/encrypt", json=payload)
    assert response.status_code == 200
    encrypted_data = response.json()
    keys = list(encrypted_data.keys())
    assert keys == ["name", "age", "contact"]