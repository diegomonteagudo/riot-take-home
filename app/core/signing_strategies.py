from abc import ABC, abstractmethod
import hmac, hashlib
import json

from app.models import SignatureResponse
from app.core.utils import sort_dict
from app.config import SIGNING_KEY


class SigningStrategy(ABC):
    """Abstract base class for JSON payload signing strategies.

    Subclasses should implement methods for signing and verifying
    JSON-compatible dictionaries."""

    @abstractmethod
    def sign_json_payload(self, payload: dict) -> SignatureResponse:
        """Sign the given JSON payload dictionary."""
        pass

    @abstractmethod
    def is_signature_valid(self, payload: dict, signature: str) -> bool:
        """Verify if the given signature is valid for the JSON payload."""
        pass

    def unify_payload(self, payload: dict) -> dict:
        """Returns a unified version of the payload, so that order of
        attributes is not relevant for signing/verifying. Currently
        implemented by sorting the dictionary keys at all depths."""
        return sort_dict(payload)


class HMACSigningStrategy(SigningStrategy):
    """Implementation of SigningStrategy using HMAC as the signing algorithm
    with SHA256 as the hash function."""

    def sign_json_payload(self, payload: dict) -> SignatureResponse:
        """Sign the given JSON payload dictionary using HMAC,
        independently of attribute order."""
        sorted_payload = self.unify_payload(payload)
        payload_bytes = self.serialize_payload(sorted_payload)
        payload_signature = self.generate_signature(payload_bytes)
        return SignatureResponse(signature=payload_signature)

    def is_signature_valid(self, payload: dict, signature: str) -> bool:
        """Verify if the given signature is valid HMAC signature for
        the JSON payload, independently of attribute order."""
        sorted_payload = self.unify_payload(payload)
        payload_bytes = self.serialize_payload(sorted_payload)
        expected_signature = self.generate_signature(payload_bytes)
        return self.compare_signatures(expected_signature, signature)

    def serialize_payload(self, payload: dict) -> bytes:
        """Serialize the given JSON payload dictionary into bytes."""
        return json.dumps(payload).encode("utf-8")

    def generate_signature(self, payload_bytes: bytes) -> str:
        """Generate HMAC SHA256 signature for the given payload
        in bytes using the defined SIGNING_KEY in config.py."""
        return hmac.new(
            key=SIGNING_KEY, msg=payload_bytes, digestmod=hashlib.sha256
        ).hexdigest()

    def compare_signatures(self, sig1: str, sig2: str) -> bool:
        """Compare two signatures.

        It is preferable to NOT use '==' because of
        'timing attacks', where an attacker can have info about the
        signature by studying the time it takes to compare them
        (when using ==, the comparison stops at the first different character).
        """
        return hmac.compare_digest(sig1, sig2)
