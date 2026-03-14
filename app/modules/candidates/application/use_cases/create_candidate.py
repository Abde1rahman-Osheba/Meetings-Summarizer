from app.modules.candidates.application.services.candidate_service import CandidateService


class CreateCandidate:
    def __init__(self, service: CandidateService) -> None:
        self.service = service

    def execute(self, **kwargs):
        return self.service.execute(kwargs)
