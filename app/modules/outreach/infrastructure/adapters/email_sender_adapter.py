class EmailSenderAdapter:
    def execute(self, payload: dict) -> dict:
        return {"adapter": "EmailSenderAdapter", "payload": payload}
