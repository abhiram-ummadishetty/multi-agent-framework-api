from pydantic import BaseModel
from typing import List


class AgentInfo(BaseModel):
    agent_id: str
    name: str
    type: str  # "orchestrator" | "ai-agent" | "rag-agent"
    status: str  # "active" | "idle" | "error"
    description: str
    capabilities: List[str]


class AgentListResponse(BaseModel):
    agents: List[AgentInfo]
    total: int
