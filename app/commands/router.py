"""Command router."""


class CommandRouter:
    """Routes slash commands."""

    def __init__(self):
        self._commands = {}

    def register(self, command: str, handler):
        self._commands[command] = handler

    def execute(self, message: str):
        if not message.startswith("/"):
            return None

        parts = message.split(maxsplit=1)

        command = parts[0]
        argument = parts[1] if len(parts) > 1 else ""

        handler = self._commands.get(command)

        if handler is None:
            return f"Unknown command: {command}"

        return handler(argument)

    def commands(self):
        return sorted(self._commands.keys())
