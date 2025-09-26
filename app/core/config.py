from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or `.env` files."""

    model_config = SettingsConfigDict(
        env_file=(Path(__file__).resolve().parents[2] / ".env").as_posix(),
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="CHATBOT_",
    )

    app_name: str = Field(default="Chatbot Backend")
    debug: bool = Field(default=False)
    api_v1_prefix: str = Field(default="/api/v1")

    llm_provider: Literal["openai", "anthropic", "local", "stub"] = Field(default="stub")
    openai_api_key: Optional[str] = Field(default=None)
    anthropic_api_key: Optional[str] = Field(default=None)

    database_url: str = Field(default="sqlite:///./chatbot.db")
    memory_backend: Literal["in_memory", "sqlite"] = Field(default="in_memory")

    log_level: str = Field(default="INFO")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached `Settings` instance."""

    return Settings()
