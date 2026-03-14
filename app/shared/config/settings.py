from pydantic import BaseModel

from app.shared.config.environment import Environment


class Settings(BaseModel):
    app_name: str = "PATHS"
    environment: Environment = Environment.LOCAL
    jwt_secret_key: str = "change-me"
    jwt_issuer: str = "paths-api"
    jwt_access_ttl_seconds: int = 900
    jwt_refresh_ttl_seconds: int = 604800


settings = Settings()
