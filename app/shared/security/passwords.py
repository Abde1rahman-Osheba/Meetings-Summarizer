import hashlib
import secrets


class PasswordHelper:
    @staticmethod
    def hash_password(password: str) -> str:
        salt = secrets.token_hex(8)
        digest = hashlib.sha256(f"{salt}:{password}".encode()).hexdigest()
        return f"{salt}${digest}"

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        salt, digest = password_hash.split("$", maxsplit=1)
        computed = hashlib.sha256(f"{salt}:{password}".encode()).hexdigest()
        return computed == digest
