from abc import ABC, abstractmethod
import hmac, hashlib
import json
from typing import Any

from app.models import SignatureResponse
from app.core.utils import sort_dict
from app.config import SIGNING_KEY

class SigningStrategy(ABC):
    @abstractmethod
    def sign_json_payload(self, payload: dict) -> SignatureResponse:
        pass

    def unify_payload(self, payload: dict) -> dict:
        return sort_dict(payload)


class HMACSigningStrategy(SigningStrategy):
    def sign_json_payload(self, payload: dict = None) -> SignatureResponse:
        if payload is None:
            payload = {}
        sorted_payload = self.unify_payload(payload)
        payload_bytes = self.serialize_payload(sorted_payload)
        payload_signature = self.generate_signature(payload_bytes)
        return SignatureResponse(signature=payload_signature)
    
    def serialize_payload(self, payload: dict) -> bytes:
        return json.dumps(payload).encode('utf-8')
    
    def generate_signature(self, payload_bytes: bytes) -> str:
        return hmac.new(
            key=SIGNING_KEY,
            msg=payload_bytes,
            digestmod=hashlib.sha256
        ).hexdigest()