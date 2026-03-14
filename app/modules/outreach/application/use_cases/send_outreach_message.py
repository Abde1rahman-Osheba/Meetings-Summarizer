from app.modules.outreach.application.services.outreach_service import OutreachService


class SendOutreachMessage:
    def __init__(self, service: OutreachService) -> None:
        self.service = service

    def execute(self, **kwargs):
        return self.service.execute(kwargs)
