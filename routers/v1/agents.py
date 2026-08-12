from fastapi import APIRouter, HTTPException
from schemas.agents import AgentListResponse, AgentInfo

router = APIRouter()

STUB_AGENTS = [
    AgentInfo(
        agent_id="orchestrator-01",
        name="Agent Orchestrator",
        type="orchestrator",
        status="active",
        description="Routes tasks to the appropriate AI agent.",
        capabilities=["routing", "task-decomposition", "result-aggregation"],
    ),
    AgentInfo(
        agent_id="ai-agent-01",
        name="AI Agent 1",
        type="ai-agent",
        status="active",
        description="General-purpose AI agent with LLM and MCP client.",
        capabilities=["llm-inference", "mcp-tools", "code-generation"],
    ),
    AgentInfo(
        agent_id="ai-agent-02",
        name="AI Agent 2",
        type="ai-agent",
        status="active",
        description="Specialized agent for data analysis tasks.",
        capabilities=["llm-inference", "mcp-tools", "data-analysis"],
    ),
    AgentInfo(
        agent_id="rag-agent-01",
        name="RAG Agent",
        type="rag-agent",
        status="active",
        description="Retrieval-Augmented Generation agent using vector store.",
        capabilities=["vector-search", "document-retrieval", "context-augmentation"],
    ),
]


@router.get("", response_model=AgentListResponse)
async def list_agents():
    return AgentListResponse(agents=STUB_AGENTS, total=len(STUB_AGENTS))


@router.get("/{agent_id}", response_model=AgentInfo)
async def get_agent(agent_id: str):
    for agent in STUB_AGENTS:
        if agent.agent_id == agent_id:
            return agent
    raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
