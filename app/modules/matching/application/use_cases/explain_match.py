from app.modules.matching.application.services.matching_service import MatchingService


class ExplainMatch:
    def __init__(self, service: MatchingService) -> None:
        self.service = service

    def execute(self, **kwargs):
        return self.service.execute(kwargs)
