"""Agent registry."""

from app.agents.agent import Agent


class AgentRegistry:
    """Stores and manages AI agents."""

    def __init__(self) -> None:
        self._agents: dict[str, Agent] = {}

    def register(self, agent: Agent) -> None:
        """Register an agent."""
        self._agents[agent.name] = agent

    def get(self, name: str) -> Agent | None:
        """Retrieve an agent by name."""
        return self._agents.get(name)

    def list(self) -> list[str]:
        """List all registered agents."""
        return sorted(self._agents.keys())

    def remove(self, name: str) -> bool:
        """Remove an agent."""
        return self._agents.pop(name, None) is not None
