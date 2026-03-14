from app.modules.interviews.application.services.interview_service import InterviewService


class UpdateInterviewStatus:
    def __init__(self, service: InterviewService) -> None:
        self.service = service

    def execute(self, **kwargs):
        return self.service.execute(kwargs)
