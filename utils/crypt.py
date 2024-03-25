from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from cryptography.fernet import Fernet
from core.config import salt
salt = salt.encode()

# Функция для создания ключа из пароля
def create_key_from_password(password_provided: str, salt: bytes = salt) -> bytes:
    password = password_provided.encode()  # Конвертируем пароль в тип bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = base64.urlsafe_b64encode(
        kdf.derive(password)
    )  # Может использоваться в качестве ключа
    return key


# Функция для шифрования текста
def encrypt_message(message: str, password_provided: str, salt: bytes = salt) -> str:
    key = create_key_from_password(password_provided, salt)
    cipher_suite = Fernet(key)
    encrypted_message = cipher_suite.encrypt(message.encode("utf-8"))
    encrypted_message = encrypted_message.decode(
        "utf-8"
    )  # Конвертируем результат в тип str
    return encrypted_message


# Функция для расшифровки текста
def decrypt_message(
    encrypted_message: str, password_provided: str, salt: bytes = salt
) -> str:
    key = create_key_from_password(password_provided, salt)
    cipher_suite = Fernet(key)
    decrypted_message = cipher_suite.decrypt(encrypted_message.encode("utf-8")).decode(
        "utf-8"
    )
    return decrypted_message
