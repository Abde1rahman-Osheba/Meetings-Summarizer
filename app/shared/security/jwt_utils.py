import base64
import hashlib
import hmac
import json
import time
from typing import Any


class JwtUtils:
    @staticmethod
    def encode(payload: dict[str, Any], secret: str) -> str:
        body = payload | {"iat": int(time.time())}
        raw = json.dumps(body, separators=(",", ":")).encode()
        sig = hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest().encode()
        return base64.urlsafe_b64encode(raw).decode() + "." + base64.urlsafe_b64encode(sig).decode()

    @staticmethod
    def decode(token: str, secret: str) -> dict[str, Any]:
        raw_part, sig_part = token.split(".", maxsplit=1)
        raw = base64.urlsafe_b64decode(raw_part.encode())
        sig = base64.urlsafe_b64decode(sig_part.encode()).decode()
        expected = hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            raise ValueError("Invalid signature")
        return json.loads(raw.decode())
