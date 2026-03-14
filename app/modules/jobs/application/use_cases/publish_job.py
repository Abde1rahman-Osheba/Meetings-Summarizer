from app.modules.jobs.application.services.job_service import JobService


class PublishJob:
    def __init__(self, service: JobService) -> None:
        self.service = service

    def execute(self, **kwargs):
        return self.service.execute(kwargs)
