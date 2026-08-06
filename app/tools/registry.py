"""Tool registry."""

from app.tools.tool import Tool


class ToolRegistry:
    """Stores tools."""

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool

    def get(self, name: str):
        return self._tools.get(name)

    def list(self):
        return sorted(self._tools.keys())

    def remove(self, name: str):
        return self._tools.pop(name, None) is not None
