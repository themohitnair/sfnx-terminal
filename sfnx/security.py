from argon2 import PasswordHasher
from argon2 import Type
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

ph = PasswordHasher(
    time_cost=2,
    memory_cost=102400,
    parallelism=8,
    hash_len=32,
    type=Type.ID
)

def derive_key(m_password: str) -> bytes:
    hashed_key = ph.hash(m_password)
    return hashed_key.encode()[:32]

def encrypt(key: bytes, plaintext: str) -> bytes:
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes long")
    
    iv = os.urandom(16)
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    return iv + encrypted_data

def decrypt(key: bytes, encrypted_data: bytes) -> str:
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes long")
    
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    padded_plaintext = decryptor.update(encrypted_data) + decryptor.finalize()
    
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    
    return plaintext.decode()

if __name__ == "__main__":
    pwd = input("Enter the password to generate key: ")
    key = derive_key(pwd)
    secret = input("Enter the secret: ")
    encrypted = encrypt(key, secret)
    print(f"Encrypted data (in bytes): {encrypted}")
    decrypted = decrypt(key, encrypted)
    print(f"Decrypted data: {decrypted}")