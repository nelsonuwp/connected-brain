"""Typed settings loaded from environment / .env file at the repo root."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# .env lives at the repo root (connected-brain/.env), not inside this project.
# Traverse: jsm_sync/config.py → jsm_sync/ → jsm-sync/ → projects/ → connected-brain/
_REPO_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_REPO_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Postgres
    database_url: str

    # Jira
    jira_base_url: str
    jira_username: str
    jira_api_token: str

    # Sync config
    jira_project: str = "APTUM"
    jira_lookback_days: int = 30
    jira_semaphore_limit: int = 5

    # Logging
    log_level: str = "INFO"


settings = Settings()
