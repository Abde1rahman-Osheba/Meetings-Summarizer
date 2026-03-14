from app.modules.auth.infrastructure.security.jwt_service import JwtService
from app.modules.auth.infrastructure.security.password_hasher import PasswordHasher


def test_password_hash_and_verify() -> None:
    hasher = PasswordHasher()
    hashed = hasher.hash('secret123')
    assert hasher.verify('secret123', hashed)


def test_token_create_and_verify() -> None:
    jwt = JwtService()
    token = jwt.create_token({'sub': 'user-1', 'role': 'admin'})
    payload = jwt.verify_token(token)
    assert payload['sub'] == 'user-1'
