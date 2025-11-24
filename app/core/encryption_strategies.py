from abc import ABC, abstractmethod
import base64
import json

class EncryptionStrategy(ABC):
    @abstractmethod
    def encrypt(self, value) -> str:
        pass

    def encrypt_json_payload(self, payload: dict) -> dict:
        if not payload:
            return {}
        return {key: self.encrypt(value) for key, value in payload.items()}


class Base64EncryptionStrategy(EncryptionStrategy):
    def encrypt(self, value) -> str:
        serialized_value = json.dumps(value)
        utf8_bytes = serialized_value.encode("utf-8")
        return base64.b64encode(utf8_bytes).decode("utf-8")
    
    