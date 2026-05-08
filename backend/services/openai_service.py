"""OpenAI 异步服务封装"""
from openai import AsyncOpenAI
from backend.config import get_settings


class OpenAIService:
    def __init__(self):
        settings = get_settings()
        client_kwargs = {"api_key": settings.openai_api_key}
        if settings.openai_api_base:
            client_kwargs["base_url"] = settings.openai_api_base
        self.client = AsyncOpenAI(**client_kwargs)
        self.model = settings.openai_model
        self.temperature = settings.openai_temperature
        self.max_tokens = settings.openai_max_tokens

    async def chat_completion(self, messages: list[dict]) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content
