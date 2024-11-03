import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

load_dotenv()

class CryptService:
    def __init__(self):
        self.key = bytes.fromhex(os.getenv('CRYPTO_KEY'))
        self.backend = default_backend()

    def encrypt(self, plaintext: str) -> str:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()

        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return (iv + encrypted).hex()

    def decrypt(self, encrypted_text: str) -> str:
        encrypted_data = bytes.fromhex(encrypted_text)
        iv = encrypted_data[:16]
        encrypted_message = encrypted_data[16:]

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()

        decrypted_padded = decryptor.update(encrypted_message) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

        return decrypted.decode()