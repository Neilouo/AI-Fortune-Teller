"""Agent 抽象基类"""
from abc import ABC, abstractmethod
from backend.core.emotion_engine import EmotionEngine
from backend.services.openai_service import OpenAIService


class BaseAgent(ABC):
    def __init__(self, openai_service: OpenAIService, emotion_engine: EmotionEngine):
        self.openai = openai_service
        self.emotion_engine = emotion_engine

    @property
    @abstractmethod
    def agent_id(self) -> str:
        ...

    @property
    @abstractmethod
    def display_name(self) -> str:
        ...

    @property
    @abstractmethod
    def icon(self) -> str:
        ...

    @property
    @abstractmethod
    def color(self) -> str:
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        ...

    @abstractmethod
    def get_system_prompt(self, bazi_context: str, emotion: str, intensity: float) -> str:
        ...

    @abstractmethod
    def get_knowledge_context(self, topic: str) -> str:
        ...

    async def chat(
        self,
        user_message: str,
        bazi_context: str,
        conversation_history: list[dict],
        emotion: str,
        intensity: float,
        topic: str,
    ) -> str:
        system_prompt = self.get_system_prompt(bazi_context, emotion, intensity)
        knowledge = self.get_knowledge_context(topic)
        if knowledge:
            system_prompt += f"\n\n【相关智慧参考】\n{knowledge}"

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history[-20:])
        messages.append({"role": "user", "content": user_message})

        response = await self.openai.chat_completion(messages)
        response = self.emotion_engine.enhance_dialogue_fluency(response, emotion)
        return response
