from pydantic import BaseModel
from typing import List


class AgentInfo(BaseModel):
    agent_id: str
    name: str
    type: str
    status: str
    description: str
    capabilities: List[str]


class AgentListResponse(BaseModel):
    agents: List[AgentInfo]
    total: int


__all__ = ["AgentInfo", "AgentListResponse"]
