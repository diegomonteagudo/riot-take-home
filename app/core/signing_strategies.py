from abc import ABC, abstractmethod
import hmac, hashlib
import json

from app.models import SignatureResponse
from app.core.utils import sort_dict
from app.config import SIGNING_KEY

class SigningStrategy(ABC):
    @abstractmethod
    def sign_json_payload(self, payload: dict) -> SignatureResponse:
        pass

    @abstractmethod
    def is_signature_valid(self, payload: dict, signature: str) -> bool:
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
    
    
    def is_signature_valid(self, payload: dict, signature: str) -> bool:
        sorted_payload = self.unify_payload(payload)
        payload_bytes = self.serialize_payload(sorted_payload)
        expected_signature = self.generate_signature(payload_bytes)
        return self.compare_signatures(expected_signature, signature)
    

    def serialize_payload(self, payload: dict) -> bytes:
        return json.dumps(payload).encode('utf-8')
    

    def generate_signature(self, payload_bytes: bytes) -> str:
        return hmac.new(
            key=SIGNING_KEY,
            msg=payload_bytes,
            digestmod=hashlib.sha256
        ).hexdigest()
    

    def compare_signatures(self, sig1: str, sig2: str) -> bool:
        """ Compare two signatures. 
        
        It is preferable to NOT use '==' because of
        'timing attacks', where an attacker can have info about the 
        signature by studying the time it takes to compare them
        (when using ==, the comparison stops at the first different character).
        """
        return hmac.compare_digest(sig1, sig2)