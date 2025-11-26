import json
import hmac, hashlib
from fastapi.testclient import TestClient

from app.main import app
from app.config import SIGNING_KEY

client = TestClient(app)


def generate_hmac_signature(payload: dict) -> str:
    """ Generate HMAC SHA256 signature for the given payload using SIGNING_KEY.
    
    Warning : this helper function is only for the tests and 
    does not sort the payload like the API does."""
    payload_bytes = json.dumps(payload).encode('utf-8')
    signature = hmac.new(SIGNING_KEY, payload_bytes, hashlib.sha256).hexdigest()
    return signature


def test_sign_no_payload():
    response = client.post("/sign")
    assert response.status_code == 200
    assert response.json() == {"signature": generate_hmac_signature({})}


def test_sign_empty_payload():
    response = client.post("/sign", json={})
    assert response.status_code == 200
    assert response.json() == {"signature": generate_hmac_signature({})}


def test_sign_not_json():
    response = client.post("/sign", content="Not a JSON")
    assert response.status_code == 422


def test_sign_valid():
    payload = {
        "message": "Hello World",
        "timestamp": 1616161616
    }
    response = client.post("/sign", json=payload)
    assert response.status_code == 200
    signature = generate_hmac_signature(payload)
    assert response.json() == {"signature": signature}


def test_sign_null_values():
    payload = {
        "message": None,
        "timestamp": 1616161616
    }
    response = client.post("/sign", json=payload)
    assert response.status_code == 200
    signature = generate_hmac_signature(payload)
    assert response.json() == {"signature": signature}


def test_sign_boolean_values():
    payload = {
        "alive": True,
        "well": False
    }
    response = client.post("/sign", json=payload)
    assert response.status_code == 200
    signature = generate_hmac_signature(payload)
    assert response.json() == {"signature": signature}


def test_sign_different_order():
    payload1 = {
        "message": "Hello World",
        "timestamp": 1616161616
    }
    payload2 = {
        "timestamp": 1616161616,
        "message": "Hello World"
    }
    response1 = client.post("/sign", json=payload1)
    response2 = client.post("/sign", json=payload2)
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json() == response2.json()


def test_sign_nested_json():
    # Manually sorted for the test
    payload = {
        "age": 30,
        "contact": {
            "coordinates": {
                "lat": 48.856364,
                "long": 2.364366
            },
            "email": "john@example.com",
            "phone": "123-456-7890"
        },
        "name": "John Doe"
    }
    response = client.post("/sign", json=payload)
    assert response.status_code == 200
    signature = generate_hmac_signature(payload)
    assert response.json() == {"signature": signature}


def test_sign_nested_json_different_order():
    payload1 = {
        "contact": {
            "phone": "123-456-7890",
            "email": "john@example.com"
        }
    }
    payload2 = {
        "contact": {
            "email": "john@example.com",
            "phone": "123-456-7890"
        }
    }
    response1 = client.post("/sign", json=payload1)
    response2 = client.post("/sign", json=payload2)
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json() == response2.json()


def test_sign_list_values():
    payload = {
        "items": [1, "2", [3, 4], {"key": "value"}]
    }
    response = client.post("/sign", json=payload)
    assert response.status_code == 200
    signature = generate_hmac_signature(payload)
    assert response.json() == {"signature": signature}


def test_sign_list_values_different_order():
    payload1 = {
        "items": [1, "2", [3, 4], {"key": "value"}]
    }
    payload2 = {
        "items": [{"key": "value"}, [3, 4], "2", 1]
    }
    response1 = client.post("/sign", json=payload1)
    response2 = client.post("/sign", json=payload2)
    assert response1.status_code == 200
    assert response2.status_code == 200
    # Order in lists do matter semantically so different signature
    assert response1.json() != response2.json()