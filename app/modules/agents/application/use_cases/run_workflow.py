from app.modules.agents.application.services.agent_orchestrator import AgentOrchestrator


class RunWorkflow:
    def __init__(self, service: AgentOrchestrator) -> None:
        self.service = service

    def execute(self, **kwargs):
        return self.service.execute(kwargs)
