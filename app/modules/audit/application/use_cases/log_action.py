from app.modules.audit.application.services.audit_service import AuditService


class LogAction:
    def __init__(self, service: AuditService) -> None:
        self.service = service

    def execute(self, **kwargs):
        return self.service.execute(kwargs)
