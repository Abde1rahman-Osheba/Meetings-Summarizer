class SqlAnalyticsRepository:
    def __init__(self) -> None:
        self._records: dict[str, dict] = {}

    def save(self, key: str, data: dict) -> None:
        self._records[key] = data

    def get(self, key: str):
        return self._records.get(key)
