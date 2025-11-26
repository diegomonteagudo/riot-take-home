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


def format_payload(signature: str, data: dict) -> dict:
    return {
        "data": data,
        "signature": signature
    }


def test_verify_no_payload():
    response = client.post("/verify")
    assert response.status_code == 422
    # Verification requires both payload and signature


def test_verify_empty_payload():
    response = client.post("/verify", json={})
    assert response.status_code == 422


def test_verify_not_json():
    response = client.post("/verify", content="Not a JSON")
    assert response.status_code == 422


def test_verify_signature_but_no_data():
    response = client.post("/verify", json={"signature": "abc"})
    assert response.status_code == 422


def test_verify_data_but_no_signature():
    response = client.post("/verify", json={"data": {"key": "value"}})
    assert response.status_code == 422


def test_verify_valid_signature():
    payload = {
        "message": "Hello World",
        "timestamp": 1616161616
    }
    signature = generate_hmac_signature(payload)
    request_body = format_payload(signature, payload)
    response = client.post("/verify", json=request_body)
    assert response.status_code == 204


def test_verify_valid_different_orders():
    payload1 = {
        "message": "Hello World",
        "timestamp": 1616161616
    }
    payload2 = {
        "timestamp": 1616161616,
        "message": "Hello World"
    }
    signature = generate_hmac_signature(payload1)
    request_body1 = format_payload(signature, payload1)
    request_body2 = format_payload(signature, payload2)
    response1 = client.post("/verify", json=request_body1)
    response2 = client.post("/verify", json=request_body2)
    assert response1.status_code == 204
    assert response2.status_code == 204


def test_verify_valid_different_orders_nested():
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
    signature = generate_hmac_signature(payload1)
    request_body1 = format_payload(signature, payload1)
    request_body2 = format_payload(signature, payload2)
    response1 = client.post("/verify", json=request_body1)
    response2 = client.post("/verify", json=request_body2)
    assert response1.status_code == 204
    assert response2.status_code == 204


def test_verify_invalid_tampered_signature():
    payload = {
        "message": "Hello World",
        "timestamp": 1616161616
    }
    signature = generate_hmac_signature(payload)
    # Tamper with the signature
    wrong_char = '0' if signature[-1] != '0' else '1'
    tampered_signature = signature[:-1] + wrong_char
    request_body = format_payload(tampered_signature, payload)
    response = client.post("/verify", json=request_body)
    assert response.status_code == 400


def test_verify_invalid_tampered_data():
    payload = {
        "message": "Hello World",
        "timestamp": 1616161616
    }
    signature = generate_hmac_signature(payload)
    # Tamper with the data
    tampered_payload = {
        "message": "Hello World!",
        "timestamp": 1616161616
    }
    request_body = format_payload(signature, tampered_payload)
    response = client.post("/verify", json=request_body)
    assert response.status_code == 400


def test_verify_sign_then_verify():
    payload = {
        "message": "Hello World",
        "timestamp": 1616161616
    }
    sign_response = client.post("/sign", json=payload)
    assert sign_response.status_code == 200
    signature = sign_response.json().get("signature")
    request_body = format_payload(signature, payload)
    verify_response = client.post("/verify", json=request_body)
    assert verify_response.status_code == 204


def test_verify_sign_then_verify_different_order():
    payload_sign = {
        "message": "Hello World",
        "timestamp": 1616161616
    }
    payload_verify = {
        "timestamp": 1616161616,
        "message": "Hello World"
    }
    sign_response = client.post("/sign", json=payload_sign)
    assert sign_response.status_code == 200
    signature = sign_response.json().get("signature")
    request_body = format_payload(signature, payload_verify)
    verify_response = client.post("/verify", json=request_body)
    assert verify_response.status_code == 204