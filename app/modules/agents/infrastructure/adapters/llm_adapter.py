class LlmAdapter:
    def execute(self, payload: dict) -> dict:
        return {"adapter": "LlmAdapter", "payload": payload}
