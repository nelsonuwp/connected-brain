"""Typed settings loaded from the connected-brain root .env."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# ops_agent/config.py → ops_agent/ → ops-agent/ → projects/ → connected-brain/
_REPO_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_REPO_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Postgres — same instance as jsm-sync
    database_url: str

    # OpenRouter
    openrouter_api_key: str
    model_workhorse: str = "anthropic/claude-sonnet-4-5"
    temperature_workhorse: float = 0.4
    llm_max_retries: int = 3

    # Server
    ops_agent_host: str = "127.0.0.1"
    ops_agent_port: int = 8080

    # Logging
    log_level: str = "INFO"


settings = Settings()
