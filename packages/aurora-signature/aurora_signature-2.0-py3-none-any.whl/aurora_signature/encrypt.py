from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import base64

def generate_key(password: str, salt: bytes) -> bytes:
    return PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)

def encrypt_data(data: bytes, password: str) -> str:
    salt = get_random_bytes(16)
    key = generate_key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return base64.urlsafe_b64encode(salt + cipher.nonce + tag + ciphertext).decode('utf-8')

def decrypt_data(encrypted_data: str, password: str) -> bytes:
    encrypted_bytes = base64.urlsafe_b64decode(encrypted_data)
    salt = encrypted_bytes[:16]
    nonce = encrypted_bytes[16:32]
    tag = encrypted_bytes[32:48]
    ciphertext = encrypted_bytes[48:]
    
    key = generate_key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
