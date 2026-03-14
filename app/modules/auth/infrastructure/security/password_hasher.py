from app.shared.security.passwords import PasswordHelper


class PasswordHasher:
    def hash(self, password: str) -> str:
        return PasswordHelper.hash_password(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        return PasswordHelper.verify_password(password, hashed_password)
