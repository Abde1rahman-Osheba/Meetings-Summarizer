from app.modules.rag.application.services.rag_service import RagService


class RetrieveContext:
    def __init__(self, service: RagService) -> None:
        self.service = service

    def execute(self, **kwargs):
        return self.service.execute(kwargs)
