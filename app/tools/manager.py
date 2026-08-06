"""Tool manager."""

from app.tools import executor, registry


class ToolManager:
    """High-level tool interface."""

    def available(self):
        return registry.list()

    def execute(self, name: str, *args):
        return executor.execute(name, *args)


manager = ToolManager()
