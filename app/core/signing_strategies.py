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
        # Make serialization NOT dependent on attribute order by sorting them
        sorted_payload = self.unify_payload(payload)
        payload_bytes = json.dumps(sorted_payload).encode('utf-8')
        signature = hmac.new(
            key=SIGNING_KEY,
            msg=payload_bytes,
            digestmod=hashlib.sha256
        ).hexdigest()
        return SignatureResponse(signature=signature)