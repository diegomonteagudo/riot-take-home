from fastapi import APIRouter
import base64
import json

router = APIRouter()

@router.post("/encrypt")
def encrypt_payload(payload: dict = None):
    if not payload:
        return {}

    def encrypt_value(value):
        if value is None:
            value = "null"
        elif isinstance(value, bool):
            value = str(value).lower()
        elif not isinstance(value, str):
            value = json.dumps(value)
        if isinstance(value, str):
            value = value.encode("utf-8")
        return base64.b64encode(value).decode("utf-8")

    encrypted_payload = {key: encrypt_value(value) for key, value in payload.items()}
    return encrypted_payload