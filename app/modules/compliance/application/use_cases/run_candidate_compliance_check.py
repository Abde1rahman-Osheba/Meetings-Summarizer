from app.modules.compliance.application.services.compliance_service import ComplianceService


class RunCandidateComplianceCheck:
    def __init__(self, service: ComplianceService) -> None:
        self.service = service

    def execute(self, **kwargs):
        return self.service.execute(kwargs)
