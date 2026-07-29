import base64
from cryptography.fernet import Fernet
from app.core.config import settings

def get_fernet() -> Fernet:
    # Ensure key is 32 URL-safe base64-encoded bytes
    key_str = settings.ENCRYPTION_KEY
    if not key_str:
        raise ValueError("ENCRYPTION_KEY is not set in configuration")
    
    # Pad to make it valid for base64 if it isn't
    try:
        key = base64.urlsafe_b64decode(key_str)
        if len(key) != 32:
            # Just create a consistent 32-byte key from it
            key = key_str.encode('utf-8')[:32].ljust(32, b'0')
            return Fernet(base64.urlsafe_b64encode(key))
        return Fernet(key_str.encode('utf-8'))
    except Exception:
        # Fallback to simple padding
        key = key_str.encode('utf-8')[:32].ljust(32, b'0')
        return Fernet(base64.urlsafe_b64encode(key))

def encrypt_password(password: str) -> str:
    if not password:
        return ""
    f = get_fernet()
    return f.encrypt(password.encode('utf-8')).decode('utf-8')

def decrypt_password(encrypted_password: str) -> str:
    if not encrypted_password:
        return ""
    f = get_fernet()
    return f.decrypt(encrypted_password.encode('utf-8')).decode('utf-8')
