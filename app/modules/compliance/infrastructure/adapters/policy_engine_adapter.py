class PolicyEngineAdapter:
    def execute(self, payload: dict) -> dict:
        return {"adapter": "PolicyEngineAdapter", "payload": payload}
