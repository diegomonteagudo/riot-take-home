from fastapi import APIRouter, HTTPException

from app.core.encryption_strategies import Base64EncryptionStrategy
from app.core.signing_strategies import HMACSigningStrategy
from app.models import SignatureResponse, VerifyRequest

router = APIRouter()
encryption_strategy = Base64EncryptionStrategy()
signing_strategy = HMACSigningStrategy()

@router.post("/encrypt", summary="Encrypt any JSON payload")
def encrypt(payload: dict) -> dict:
    """ Encrypt all first-depth values in any given JSON payload. """
    return encryption_strategy.encrypt_json_payload(payload)

@router.post("/decrypt", summary="Decrypt any JSON payload")
def decrypt(payload: dict) -> dict:
    """ Decrypt all first-depth values in any given JSON payload"""
    return encryption_strategy.decrypt_json_payload(payload)

@router.post("/sign", response_model=SignatureResponse, 
             summary="Sign any JSON payload")
def sign(payload: dict) -> SignatureResponse:
    """ Sign any given JSON payload based on its value (order independent)
    and return its signature."""
    return signing_strategy.sign_json_payload(payload)

@router.post("/verify", status_code=204, 
             summary="Verify the signature of any JSON payload")
def verify(payload: VerifyRequest) -> None:
    payload_data = payload.data
    payload_signature = payload.signature
    if not signing_strategy.is_signature_valid(payload_data, payload_signature):
        raise HTTPException(status_code=400, detail="Invalid signature")