import base64
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend

class KeyManager:
    """
    A class for managing AES keys, including generation, derivation from passwords, and secure storage.
    """

    @staticmethod
    def generate_key():
        """Generates a random 256-bit AES key."""
        return os.urandom(32)

    @staticmethod
    def derive_key_from_password(password: str, salt: bytes) -> bytes:
        """
        Derives a 256-bit AES key from a password using PBKDF2-HMAC with SHA-256.

        Args:
            password (str): The password to derive the key from.
            salt (bytes): A random salt value to make key derivation unique.

        Returns:
            bytes: A 256-bit key derived from the password.
        """
        kdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,  # 256 bits
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password.encode('utf-8'))

    @staticmethod
    def save_key_to_file(key: bytes, filepath: str):
        """
        Saves an AES key to a file in a secure format (Base64 encoded).

        Args:
            key (bytes): The AES key to save.
            filepath (str): The path to the file to save the key.
        """
        with open(filepath, 'wb') as f:
            f.write(base64.b64encode(key))

    @staticmethod
    def load_key_from_file(filepath: str) -> bytes:
        """
        Loads an AES key from a file (Base64 encoded).

        Args:
            filepath (str): The path to the file containing the AES key.

        Returns:
            bytes: The loaded AES key.
        """
        with open(filepath, 'rb') as f:
            return base64.b64decode(f.read())
