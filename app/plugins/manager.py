"""Plugin manager."""

from app.plugins.plugin import Plugin


class PluginManager:
    """Stores loaded plugins."""

    def __init__(self):
        self._plugins: dict[str, Plugin] = {}

    def register(self, plugin: Plugin) -> None:
        plugin.setup()
        self._plugins[plugin.name] = plugin

    def get(self, name: str):
        return self._plugins.get(name)

    def list(self):
        return sorted(self._plugins.keys())

    def remove(self, name: str):
        return self._plugins.pop(name, None) is not None


manager = PluginManager()
