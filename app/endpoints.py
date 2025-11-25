from fastapi import APIRouter

from app.core.encryption_strategies import Base64EncryptionStrategy
from app.core.signing_strategies import HMACSigningStrategy
from app.models import SignatureResponse

router = APIRouter()
encryption_strategy = Base64EncryptionStrategy()
signing_strategy = HMACSigningStrategy()

@router.post("/encrypt")
def encrypt(payload: dict = None) -> dict:
    return encryption_strategy.encrypt_json_payload(payload)

@router.post("/decrypt")
def decrypt(payload: dict = None) -> dict:
    return encryption_strategy.decrypt_json_payload(payload)

@router.post("/sign", response_model=SignatureResponse)
def sign(payload: dict = None) -> SignatureResponse:
    return signing_strategy.sign_json_payload(payload)