"""Tool execution engine."""

from app.tools.registry import ToolRegistry


class ToolExecutor:
    """Executes registered tools."""

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def execute(self, tool_name: str, *args, **kwargs):
        tool = self.registry.get(tool_name)

        if tool is None:
            raise ValueError(f"Unknown tool: {tool_name}")

        return tool.run(*args, **kwargs)
