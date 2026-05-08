"""Agent 编排器 - 并行调度多个宗教 Agent"""
import asyncio
from backend.agents.base_agent import BaseAgent
from backend.agents.agent_registry import AGENT_REGISTRY
from backend.core.emotion_engine import EmotionEngine
from backend.services.openai_service import OpenAIService
from backend.models.schemas import AgentResponse, ChatResponse


class AgentOrchestrator:
    def __init__(self, openai_service: OpenAIService, emotion_engine: EmotionEngine):
        self.openai_service = openai_service
        self.emotion_engine = emotion_engine
        self.agents: dict[str, BaseAgent] = {}
        self._init_agents()

    def _init_agents(self):
        for agent_id, agent_cls in AGENT_REGISTRY.items():
            self.agents[agent_id] = agent_cls(
                openai_service=self.openai_service,
                emotion_engine=self.emotion_engine,
            )

    def get_agent_list(self) -> list[dict]:
        return [
            {
                "agent_id": agent.agent_id,
                "display_name": agent.display_name,
                "icon": agent.icon,
                "color": agent.color,
                "description": agent.description,
            }
            for agent in self.agents.values()
        ]

    async def dispatch(
        self,
        user_message: str,
        selected_agents: list[str],
        bazi_context: str,
        conversation_histories: dict[str, list[dict]],
    ) -> ChatResponse:
        emotion, intensity = self.emotion_engine.analyze_emotion(user_message)
        topics = self.emotion_engine.detect_topic(user_message)
        topic = topics[0] if topics else "综合"

        async def _call_agent(agent_id: str) -> AgentResponse:
            agent = self.agents[agent_id]
            history = conversation_histories.get(agent_id, [])
            try:
                response_text = await agent.chat(
                    user_message=user_message,
                    bazi_context=bazi_context,
                    conversation_history=history,
                    emotion=emotion,
                    intensity=intensity,
                    topic=topic,
                )
                return AgentResponse(
                    agent_id=agent_id,
                    display_name=agent.display_name,
                    icon=agent.icon,
                    content=response_text,
                    error=None,
                )
            except Exception as e:
                return AgentResponse(
                    agent_id=agent_id,
                    display_name=agent.display_name,
                    icon=agent.icon,
                    content="",
                    error=str(e),
                )

        tasks = [_call_agent(aid) for aid in selected_agents if aid in self.agents]
        results = await asyncio.gather(*tasks)

        return ChatResponse(
            user_message=user_message,
            emotion=emotion,
            emotion_intensity=intensity,
            topic=topic,
            responses=list(results),
        )
