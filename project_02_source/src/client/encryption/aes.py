from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os

class AESUtil:
    """Utility class for AES encryption and decryption."""

    @staticmethod
    def generate_key():
        """Generates a random 256-bit key for AES encryption."""
        return os.urandom(32)  # 32 bytes = 256 bits

    @staticmethod
    def encrypt(data: bytes, key: bytes) -> dict:
        """
        Encrypts data using AES-GCM.

        Args:
            data (bytes): The plaintext data to encrypt.
            key (bytes): The 256-bit AES key.

        Returns:
            dict: Contains the ciphertext, nonce, and authentication tag.
        """
        # Generate a random nonce (12 bytes recommended for GCM)
        nonce = os.urandom(12)

        # Initialize AES-GCM cipher
        aesgcm = AESGCM(key)
        
        # Encrypt the data
        ciphertext = aesgcm.encrypt(nonce, data, None)  # No additional authenticated data (AAD)

        return {
            'ciphertext': ciphertext,
            'nonce': nonce
        }

    @staticmethod
    def decrypt(encrypted_data: dict, key: bytes) -> bytes:
        """
        Decrypts data using AES-GCM.

        Args:
            encrypted_data (dict): Contains the ciphertext and nonce.
            key (bytes): The 256-bit AES key.

        Returns:
            bytes: The decrypted plaintext data.
        """
        # Extract nonce and ciphertext
        nonce = encrypted_data['nonce']
        ciphertext = encrypted_data['ciphertext']

        # Initialize AES-GCM cipher
        aesgcm = AESGCM(key)

        # Decrypt the data
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)  # No additional authenticated data (AAD)

        return plaintext

# Example usage
if __name__ == "__main__":
    # Generate a key
    key = AESUtil.generate_key()
    print(f"Generated Key: {key.hex()}")

    # Data to encrypt
    data = b"This is a secret note."
    print(f"Original Data: {data}")

    # Encrypt the data
    encrypted = AESUtil.encrypt(data, key)
    print(f"Encrypted Data: {encrypted}")

    # Decrypt the data
    decrypted = AESUtil.decrypt(encrypted, key)
    print(f"Decrypted Data: {decrypted}")