"""Typed settings loaded from the connected-brain root .env."""

from pathlib import Path

from pydantic import AliasChoices, Field
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

    # MSSQL BI (DM_BusinessInsights) — optional until T-context is wired; required for smoke test
    mssql_bi_server: str | None = Field(
        default=None,
        validation_alias=AliasChoices("MSSQL_BI_SERVER", "OCEAN_DB_SERVER"),
    )
    mssql_bi_name: str | None = Field(
        default=None,
        validation_alias=AliasChoices("MSSQL_BI_NAME", "OCEAN_DB_NAME"),
    )
    mssql_bi_user: str | None = Field(
        default=None,
        validation_alias=AliasChoices("MSSQL_BI_USER", "OCEAN_DB_USERNAME"),
    )
    mssql_bi_pass: str | None = Field(
        default=None,
        validation_alias=AliasChoices("MSSQL_BI_PASS", "OCEAN_DB_PASSWORD"),
    )

    # Fusion PostgreSQL (via SSH tunnel) — optional until wired; required for fusion smoke
    fusion_db_server: str | None = Field(default=None, validation_alias="FUSION_DB_SERVER")
    fusion_db_port: int = Field(default=5432, validation_alias="FUSION_DB_PORT")
    fusion_db_name: str | None = Field(default=None, validation_alias="FUSION_DB_NAME")
    fusion_db_user: str | None = Field(default=None, validation_alias="FUSION_DB_USER")
    fusion_db_pass: str | None = Field(default=None, validation_alias="FUSION_DB_PASS")

    ssh_host: str | None = Field(default=None, validation_alias="SSH_HOST")
    ssh_port: int = Field(default=22, validation_alias="SSH_PORT")
    ssh_user: str | None = Field(
        default=None,
        validation_alias=AliasChoices("SSH_USER", "SSH_USERNAME"),
    )
    ssh_pass: str | None = Field(
        default=None,
        validation_alias=AliasChoices("SSH_PASS", "SSH_PASSWORD"),
    )


settings = Settings()
