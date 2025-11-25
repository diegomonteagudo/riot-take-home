from fastapi import APIRouter

from app.core.encryption_strategies import Base64EncryptionStrategy

router = APIRouter()
strategy = Base64EncryptionStrategy()

@router.post("/encrypt")
def encrypt(payload: dict = None) -> dict:
    return strategy.encrypt_json_payload(payload)

@router.post("/decrypt")
def decrypt(payload: dict = None) -> dict:
    return strategy.decrypt_json_payload(payload)