import base64
import logging
from hashlib import sha256
from typing import Optional

from cryptography.fernet import Fernet


class EncryptionRegistry:

    KEY_LENGTH = 32

    def __init__(self, key: Optional[str] = None):
        """
        Initialize with a base64-encoded key or generate a new one.

        Args:
            key: Optional base64-encoded key. If not provided, generates a new one.
        """
        if key:
            try:
                decoded = base64.b64decode(key)
                if len(decoded) != self.KEY_LENGTH:
                    raise ValueError("Invalid key length")
                self._key = key
            except Exception as e:
                raise ValueError(f"Invalid encryption key: {e!s}")
        else:
            # Generate a new key - but warn that this is for testing only
            # logging.warning(
            #     "No encryption key provided - generating a new one. "
            #     "This should only be used for testing."
            # )
            self._key = Fernet.generate_key().decode()

        self._fernet = Fernet(self._key.encode())

        # Create a test value to verify key compatibility
        self._test_token = self.encrypt("test")

    def encrypt(self, value: str) -> str:
        """
        Encrypt a value
        Returns: base64-encoded encrypted string
        """
        try:
            encrypted = self._fernet.encrypt(str(value).encode())
            return base64.b64encode(encrypted).decode()
        except Exception as e:
            raise ValueError(f"Encryption error: {e!s}")

    def decrypt(self, value: str) -> str:
        """
        Decrypt a base64-encoded encrypted value
        Returns: original string
        """
        try:
            encrypted = base64.b64decode(value)
            decrypted = self._fernet.decrypt(encrypted)
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Decryption error: {e!s}")

    def verify_key_compatibility(self, encrypted_data: str) -> bool:
        """
        Verify if this registry can decrypt the given encrypted data.
        Useful for testing if two registries share the same key.
        """
        try:
            self.decrypt(encrypted_data)
            return True
        except Exception:
            logging.warning("Key compatibility test failed", exc_info=True)
            return False

    @staticmethod
    def basic_hash(value: str) -> str:
        """
        Basic hash function for testing purposes.
        """
        return sha256(str(value).encode()).hexdigest()
