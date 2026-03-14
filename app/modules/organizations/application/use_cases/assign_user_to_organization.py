from app.modules.organizations.application.services.organization_service import OrganizationService


class AssignUserToOrganization:
    def __init__(self, service: OrganizationService) -> None:
        self.service = service

    def execute(self, **kwargs):
        return self.service.execute(kwargs)
