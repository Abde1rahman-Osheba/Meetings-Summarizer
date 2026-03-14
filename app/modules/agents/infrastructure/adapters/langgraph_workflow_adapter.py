class LanggraphWorkflowAdapter:
    def execute(self, payload: dict) -> dict:
        return {"adapter": "LanggraphWorkflowAdapter", "payload": payload}
