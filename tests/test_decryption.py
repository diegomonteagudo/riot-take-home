import base64
import json
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def toBase64(s):
    s = json.dumps(s).encode("utf-8")
    return base64.b64encode(s).decode("utf-8")


def test_decryption_no_payload():
    response = client.post("/decrypt")
    assert response.status_code == 422


def test_decryption_empty_payload():
    response = client.post("/decrypt", json={})
    assert response.status_code == 200
    assert response.json() == {}


def test_decryption_not_json():
    response = client.post("/decrypt", content="Not a JSON")
    assert response.status_code == 422


def test_decryption_1_attribute():
    payload = {"name": toBase64("John Doe")}
    response = client.post("/decrypt", json=payload)
    assert response.status_code == 200
    decrypted_data = response.json().get("name")
    assert decrypted_data == "John Doe"


def test_decryption_2_attributes():
    payload = {"name": toBase64("John Doe"), "age": toBase64(30)}
    response = client.post("/decrypt", json=payload)
    assert response.status_code == 200
    decrypted_data = response.json()
    assert decrypted_data.get("name") == "John Doe"
    assert decrypted_data.get("age") == 30


def test_decryption_null_value():
    payload = {"name": toBase64(None)}
    response = client.post("/decrypt", json=payload)
    assert response.status_code == 200
    decrypted_data = response.json().get("name")
    assert decrypted_data is None


def test_decryption_boolean_value():
    payload = {"alive": toBase64(True)}
    response = client.post("/decrypt", json=payload)
    assert response.status_code == 200
    decrypted_data = response.json().get("alive")
    assert decrypted_data is True


def test_decryption_list_value():
    payload = {"items": toBase64([1, 2, 3])}
    response = client.post("/decrypt", json=payload)
    assert response.status_code == 200
    decrypted_data = response.json().get("items")
    assert decrypted_data == [1, 2, 3]


def test_encryption_only_first_depth():
    payload = {
        "contact": toBase64({
            "email": "john@example.com",
            "phone": "123-456-7890"
        })
    }
    response = client.post("/decrypt", json=payload)
    assert response.status_code == 200
    decrypted_data = response.json().get("contact")
    assert decrypted_data == {
        "email": "john@example.com",
        "phone": "123-456-7890"
    }


def test_decryption_maintains_order():
    payload = {
        "name": toBase64("John Doe"),
        "age": toBase64(30),
        "contact": toBase64({
            "email": "john@example.com",
            "phone": "123-456-7890"
        })
    }
    response = client.post("/decrypt", json=payload)
    assert response.status_code == 200
    decrypted_data = response.json()
    keys = list(decrypted_data.keys())
    assert keys == ["name", "age", "contact"]


def test_encryption_then_decryption_1_attribute():
    original_payload = {"name": "John Doe"}
    encrypt_response = client.post("/encrypt", json=original_payload)
    assert encrypt_response.status_code == 200
    encrypted_data = encrypt_response.json()
    decrypt_response = client.post("/decrypt", json=encrypted_data)
    assert decrypt_response.status_code == 200
    decrypted_data = decrypt_response.json()
    assert decrypted_data == original_payload


def test_encryption_then_decryption_multiple_attributes():
    original_payload = {
        "name": "John Doe", 
        "age": 30, 
        "alive": True
    }
    encrypt_response = client.post("/encrypt", json=original_payload)
    assert encrypt_response.status_code == 200
    encrypted_data = encrypt_response.json()
    decrypt_response = client.post("/decrypt", json=encrypted_data)
    assert decrypt_response.status_code == 200
    decrypted_data = decrypt_response.json()
    assert decrypted_data == original_payload


def test_encryption_then_decryption_null():
    original_payload = {"name": None}
    encrypt_response = client.post("/encrypt", json=original_payload)
    assert encrypt_response.status_code == 200
    encrypted_data = encrypt_response.json()
    decrypt_response = client.post("/decrypt", json=encrypted_data)
    assert decrypt_response.status_code == 200
    decrypted_data = decrypt_response.json()
    assert decrypted_data == original_payload


def test_encryption_then_decryption_list():
    original_payload = {"items": [1, "2", [3]]}
    encrypt_response = client.post("/encrypt", json=original_payload)
    assert encrypt_response.status_code == 200
    encrypted_data = encrypt_response.json()
    decrypt_response = client.post("/decrypt", json=encrypted_data)
    assert decrypt_response.status_code == 200
    decrypted_data = decrypt_response.json()
    assert decrypted_data == original_payload


def test_encryption_then_decryption_nested():
    original_payload = {
        "contact": {
            "email": "john@example.com",
            "phone": "123-456-7890"
        }
    }
    encrypt_response = client.post("/encrypt", json=original_payload)
    assert encrypt_response.status_code == 200
    encrypted_data = encrypt_response.json()
    decrypt_response = client.post("/decrypt", json=encrypted_data)
    assert decrypt_response.status_code == 200
    decrypted_data = decrypt_response.json()
    assert decrypted_data == original_payload


def test_encryption_then_decryption_nested_3_levels():
    original_payload = {
        "level1": {
            "level2": {
                "level3": "deep value"
            }
        }
    }
    encrypt_response = client.post("/encrypt", json=original_payload)
    assert encrypt_response.status_code == 200
    encrypted_data = encrypt_response.json()
    decrypt_response = client.post("/decrypt", json=encrypted_data)
    assert decrypt_response.status_code == 200
    decrypted_data = decrypt_response.json()
    assert decrypted_data == original_payload

def test_already_unecrypted_value():
    payload = {"name": "John Doe"}
    response = client.post("/decrypt", json=payload)
    assert response.status_code == 200
    decrypted_data = response.json().get("name")
    assert decrypted_data == "John Doe"


def test_mixed_encrypted_and_unecrypted_values():
    payload = {
        "name": toBase64("John Doe"),
        "age": toBase64(30),
        "contact": toBase64({
            "email": "john@example.com",
            "phone": "123-456-7890"
        }),
        "birth_date": "1998-11-19"
    }
    response = client.post("/decrypt", json=payload)
    assert response.status_code == 200
    decrypted_data = response.json()
    assert decrypted_data.get("name") == "John Doe"
    assert decrypted_data.get("age") == 30
    assert decrypted_data.get("contact") == {
        "email": "john@example.com",
        "phone": "123-456-7890"
    }
    assert decrypted_data.get("birth_date") == "1998-11-19"

