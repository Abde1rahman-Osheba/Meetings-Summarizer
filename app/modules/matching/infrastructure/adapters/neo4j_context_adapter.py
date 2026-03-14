class Neo4jContextAdapter:
    def execute(self, payload: dict) -> dict:
        return {"adapter": "Neo4jContextAdapter", "payload": payload}
