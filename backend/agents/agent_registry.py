"""Agent 注册表"""
from backend.agents.buddhism_agent import BuddhismAgent
from backend.agents.taoism_agent import TaoismAgent
from backend.agents.christianity_agent import ChristianityAgent
from backend.agents.islam_agent import IslamAgent
from backend.agents.confucianism_agent import ConfucianismAgent

AGENT_REGISTRY: dict[str, type] = {
    "buddhism": BuddhismAgent,
    "taoism": TaoismAgent,
    "christianity": ChristianityAgent,
    "islam": IslamAgent,
    "confucianism": ConfucianismAgent,
}
