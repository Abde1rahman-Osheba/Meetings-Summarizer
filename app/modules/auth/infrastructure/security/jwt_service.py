from app.shared.config.settings import settings
from app.shared.security.jwt_utils import JwtUtils


class JwtService:
    def create_token(self, payload: dict) -> str:
        return JwtUtils.encode(payload, settings.jwt_secret_key)

    def verify_token(self, token: str) -> dict:
        return JwtUtils.decode(token, settings.jwt_secret_key)
