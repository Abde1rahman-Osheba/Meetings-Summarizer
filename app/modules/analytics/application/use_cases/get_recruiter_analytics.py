from app.modules.analytics.application.services.analytics_service import AnalyticsService


class GetRecruiterAnalytics:
    def __init__(self, service: AnalyticsService) -> None:
        self.service = service

    def execute(self, **kwargs):
        return self.service.execute(kwargs)
