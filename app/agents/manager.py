from typing import Any


class AgentManager:
    def __init__(self) -> None:
        self._agents: dict[str, dict[str, Any]] = {}

    def create(self, name: str, description: str = "") -> dict[str, Any]:
        if name in self._agents:
            raise ValueError(f"Agent '{name}' already exists.")

        agent = {
            "name": name,
            "description": description,
        }

        self._agents[name] = agent
        return agent

    def list(self) -> list[dict[str, Any]]:
        return list(self._agents.values())

    def get(self, name: str) -> dict[str, Any] | None:
        return self._agents.get(name)

    def delete(self, name: str) -> bool:
        return self._agents.pop(name, None) is not None


manager = AgentManager()
