from abc import ABC, abstractmethod
import base64
import json
from typing import Any


class EncryptionStrategy(ABC):
    """Abstract base class for JSON payload encryption strategies.

    Subclasses should implement methods for encrypting, decrypting,
    and checking encryption status of JSON-compatible values."""

    @abstractmethod
    def encrypt(self, value: Any) -> str:
        """Encrypt the given value."""
        pass

    @abstractmethod
    def decrypt(self, value: str) -> Any:
        """Decrypt the given string value if it is encrypted.
        Args:
            value (str): The possibly encrypted string to decrypt.
        Returns:
            Any: The original decrypted value (can be of any valid JSON type).
        """
        pass

    @abstractmethod
    def is_encrypted(self, value: str) -> bool:
        """Check if the given string value is encrypted."""
        pass

    def encrypt_json_payload(self, payload: dict) -> dict:
        """Encrypt all values in the given JSON payload dictionary."""
        if not payload:
            return {}
        return {key: self.encrypt(value) for key, value in payload.items()}

    def decrypt_json_payload(self, payload: dict) -> dict:
        """Decrypt all values in the given JSON payload dictionary
        if they are encrypted."""
        if not payload:
            return {}
        return {key: self.decrypt(value) for key, value in payload.items()}


class Base64EncryptionStrategy(EncryptionStrategy):
    """Implementation of EncryptionStrategy using Base64 encoding as
    the encryption algorithm."""

    def encrypt(self, value: Any) -> str:
        """Encrypt the given JSON value (int, str, list, dict, etc.) by
        serializing it then encoding it using Base64.
        Args:
            value: The JSON value to encrypt.
        Returns:
            str: The Base64-encoded string representation of the value.
        """
        serialized_value = json.dumps(value)
        utf8_bytes = serialized_value.encode("utf-8")
        return base64.b64encode(utf8_bytes).decode("utf-8")

    def decrypt(self, value: str) -> Any:
        """Decrypt the given value if it is a Base64-encoded JSON string.
        Args:
            value (str): The possibly encrypted string to decrypt.
        Returns:
            Any: The original decrypted value (can be of any valid JSON type).
        """
        if self.is_encrypted(value):
            serialized_json = self.decode_base64_to_serialized_json(value)
            return json.loads(serialized_json)
        return value

    def is_encrypted(self, value: str) -> bool:
        """Check if the given value is a Base64-encoded JSON string.
        In its current version, it checks if an error is raised when attempting
        to decode and parse the value.

        Potential limitation: a non-encrypted string that happens to be a valid
        Base64-encoded JSON string could be misidentified as encrypted."""
        try:
            serialized_json = self.decode_base64_to_serialized_json(value)
            json.loads(serialized_json)
            return True
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
            # The error is used to identify non-encrypted values
            return False

    def decode_base64_to_serialized_json(self, value: str) -> str:
        """Decode a string assumed to be Base64-encoded back to its
        serialized JSON representation.
        Args:
            value (str): The Base64-encoded string.
        Returns:
            str: The decoded serialized JSON string.
        """
        base64_bytes = value.encode("utf-8")
        utf8_bytes = base64.b64decode(base64_bytes)
        serialized_json = utf8_bytes.decode("utf-8")
        return serialized_json
