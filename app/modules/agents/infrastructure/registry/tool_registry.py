class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, object] = {}

    def register(self, name: str, tool: object) -> None:
        self._tools[name] = tool

    def get(self, name: str) -> object | None:
        return self._tools.get(name)
