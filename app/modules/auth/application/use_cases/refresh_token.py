from app.modules.auth.application.services.auth_service import AuthService


class RefreshToken:
    def __init__(self, service: AuthService) -> None:
        self.service = service

    def execute(self, **kwargs):
        return self.service.execute(kwargs)
