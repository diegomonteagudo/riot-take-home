from fastapi import APIRouter
import base64
import json

from app.core.encryption_strategies import Base64EncryptionStrategy

router = APIRouter()

@router.post("/encrypt")
def encrypt(payload: dict = None):
    strategy = Base64EncryptionStrategy()
    return strategy.encrypt_json_payload(payload)