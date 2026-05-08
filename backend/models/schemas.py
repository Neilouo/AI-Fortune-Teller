"""Pydantic 请求/响应模型"""
from typing import Optional
from pydantic import BaseModel


class BaziRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int


class BaziResponse(BaseModel):
    bazi: dict
    wuxing: dict
    strongest: str
    weakest: str
    zodiac: str
    constellation: str
    personality_traits: list[str]


class ChatRequest(BaseModel):
    session_id: str
    message: str
    selected_agents: list[str] = [
        "buddhism", "taoism", "christianity", "islam", "confucianism"
    ]


class AgentResponse(BaseModel):
    agent_id: str
    display_name: str
    icon: str
    content: str
    error: Optional[str] = None


class ChatResponse(BaseModel):
    user_message: str
    emotion: str
    emotion_intensity: float
    topic: str
    responses: list[AgentResponse]


class SessionCreateRequest(BaseModel):
    session_id: Optional[str] = None


class SessionCreateResponse(BaseModel):
    session_id: str


class AgentInfo(BaseModel):
    agent_id: str
    display_name: str
    icon: str
    color: str
    description: str
