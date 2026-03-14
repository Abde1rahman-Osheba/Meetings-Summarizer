class QdrantVectorStore:
    def execute(self, payload: dict) -> dict:
        return {"adapter": "QdrantVectorStore", "payload": payload}
