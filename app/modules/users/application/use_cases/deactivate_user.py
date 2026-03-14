from app.modules.users.application.services.user_service import UserService


class DeactivateUser:
    def __init__(self, service: UserService) -> None:
        self.service = service

    def execute(self, **kwargs):
        return self.service.execute(kwargs)
