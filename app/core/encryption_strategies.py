from abc import ABC, abstractmethod
import base64
import json

class EncryptionStrategy(ABC):
    @abstractmethod
    def encrypt(self, value) -> str:
        pass

    @abstractmethod
    def decrypt(self, value: str):
        pass

    def encrypt_json_payload(self, payload: dict) -> dict:
        if not payload:
            return {}
        return {key: self.encrypt(value) for key, value in payload.items()}
    
    def decrypt_json_payload(self, payload: dict) -> dict:
        if not payload:
            return {}
        return {key: self.decrypt(value) for key, value in payload.items()}


class Base64EncryptionStrategy(EncryptionStrategy):
    def encrypt(self, value) -> str:
        serialized_value = json.dumps(value)
        utf8_bytes = serialized_value.encode("utf-8")
        return base64.b64encode(utf8_bytes).decode("utf-8")
    
    def decrypt(self, value: str):
        base64_bytes = value.encode("utf-8")
        utf8_bytes = base64.b64decode(base64_bytes)
        serialized_json = utf8_bytes.decode("utf-8")
        return json.loads(serialized_json)