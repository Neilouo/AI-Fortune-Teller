"""应用配置"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 加载 backend/.env 文件
_backend_dir = Path(__file__).parent
load_dotenv(_backend_dir / ".env")


class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_model: str = "mimo-v2.5-pro"
    openai_api_base: str = "https://token-plan-sgp.xiaomimimo.com/v1"
    openai_temperature: float = 0.8
    openai_max_tokens: int = 800
    max_history_length: int = 20

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    api_key = os.getenv("OPENAI_API_KEY", "")
    model = os.getenv("OPENAI_MODEL", "mimo-v2.5-pro")
    api_base = os.getenv("OPENAI_API_BASE", "https://token-plan-sgp.xiaomimimo.com/v1")
    temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.8"))
    max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "800"))

    return Settings(
        openai_api_key=api_key,
        openai_model=model,
        openai_api_base=api_base.strip() if api_base else "",
        openai_temperature=temperature,
        openai_max_tokens=max_tokens,
    )
