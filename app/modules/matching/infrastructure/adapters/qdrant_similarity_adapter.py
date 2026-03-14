class QdrantSimilarityAdapter:
    def execute(self, payload: dict) -> dict:
        return {"adapter": "QdrantSimilarityAdapter", "payload": payload}
