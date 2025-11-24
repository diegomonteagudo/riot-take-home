from fastapi import APIRouter

from app.core.encryption_strategies import Base64EncryptionStrategy

router = APIRouter()

@router.post("/encrypt")
def encrypt(payload: dict = None):
    strategy = Base64EncryptionStrategy()
    return strategy.encrypt_json_payload(payload)

@router.post("/decrypt")
def decrypt(payload: dict = None):
    strategy = Base64EncryptionStrategy()
    return strategy.decrypt_json_payload(payload)