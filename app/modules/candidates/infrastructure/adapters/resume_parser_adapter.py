class ResumeParserAdapter:
    def execute(self, payload: dict) -> dict:
        return {"adapter": "ResumeParserAdapter", "payload": payload}
