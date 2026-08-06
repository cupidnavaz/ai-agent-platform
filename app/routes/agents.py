from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents.manager import manager

router = APIRouter(prefix="/agents", tags=["Agents"])


class AgentCreate(BaseModel):
    name: str
    description: str = ""


@router.get("/")
async def list_agents():
    return manager.list()


@router.post("/")
async def create_agent(agent: AgentCreate):
    try:
        return manager.create(agent.name, agent.description)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/{name}")
async def get_agent(name: str):
    agent = manager.get(name)

    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")

    return agent


@router.delete("/{name}")
async def delete_agent(name: str):
    if not manager.delete(name):
        raise HTTPException(status_code=404, detail="Agent not found")

    return {"deleted": True}
