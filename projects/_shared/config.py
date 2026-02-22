# projects/_shared/config.py
from pathlib import Path
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

# Always load from the root, regardless of where the script runs from
root = Path(__file__).parent.parent.parent  # up to ~/connected-brain/
load_dotenv(root / ".env")


def _env(primary: str, legacy: str | None = None, default: str | None = None) -> str | None:
    """Read env var; prefer primary name, fall back to legacy (log warning if used)."""
    val = os.getenv(primary)
    if val is not None and val != "":
        return val
    if legacy:
        leg_val = os.getenv(legacy)
        if leg_val is not None and leg_val != "":
            logger.warning(
                "Config: legacy env %s is used; migrate to %s (fallback will be removed)",
                legacy,
                primary,
            )
            return leg_val
    return default


class Config:
    # --- Jira ---
    JIRA_BASE_URL      = _env("JIRA_BASE_URL")
    JIRA_USERNAME      = _env("JIRA_USERNAME", legacy="JIRA_EMAIL")
    JIRA_EMAIL         = _env("JIRA_USERNAME", legacy="JIRA_EMAIL")  # alias
    JIRA_TOKEN         = _env("JIRA_API_TOKEN")
    JIRA_LOOKBACK_DAYS = _env("JIRA_LOOKBACK_DAYS", default="365")

    # --- Database (generic fallback) ---
    DB_HOST     = os.getenv("DB_HOST")
    DB_PORT     = os.getenv("DB_PORT", "5432")
    DB_NAME     = os.getenv("DB_NAME")
    DB_USER     = os.getenv("DB_USER")
    DB_PASSWORD = _env("DB_PASSWORD")

    # --- Salesforce ---
    SALESFORCE_DOMAIN         = _env("SALESFORCE_DOMAIN", legacy="SF_DOMAIN")
    SALESFORCE_USERNAME       = _env("SALESFORCE_USERNAME", legacy="SF_USERNAME")
    SALESFORCE_PASSWORD       = _env("SALESFORCE_PASSWORD", legacy="SF_PASSWORD")
    SALESFORCE_TOKEN          = _env("SALESFORCE_TOKEN", legacy="SF_TOKEN")
    SALESFORCE_CONSUMER_KEY   = _env("SALESFORCE_CONSUMER_KEY", legacy="SF_CONSUMER_KEY")
    SALESFORCE_CONSUMER_SECRET = _env("SALESFORCE_CONSUMER_SECRET", legacy="SF_CONSUMER_SECRET")

    # --- ZoomInfo ---
    ZOOMINFO_CLIENT_ID     = _env("ZOOMINFO_CLIENT_ID", legacy="ZI_CLIENT_ID")
    ZOOMINFO_CLIENT_SECRET = _env("ZOOMINFO_CLIENT_SECRET", legacy="ZI_CLIENT_SECRET")
    ZOOMINFO_REFRESH_TOKEN = _env("ZOOMINFO_REFRESH_TOKEN", legacy="ZI_REFRESH_TOKEN")

    # --- Ocean Database ---
    OCEAN_DB_SERVER   = _env("OCEAN_DB_SERVER", legacy="DB_SERVER")
    OCEAN_DB_NAME     = _env("OCEAN_DB_NAME", legacy="DB_NAME")
    OCEAN_DB_USERNAME = _env("OCEAN_DB_USERNAME", legacy="OCEAN_DB_USER")
    OCEAN_DB_PASSWORD = _env("OCEAN_DB_PASSWORD", legacy="DB_PASSWORD")

    # --- Azure Billing Database ---
    AZURE_BILLING_DB_NAME     = _env("AZURE_BILLING_DB_NAME", legacy="DB_NAME")
    AZURE_BILLING_DB_USERNAME  = _env("AZURE_BILLING_DB_USERNAME", legacy="AZURE_BILLING_DB_USER")
    AZURE_BILLING_DB_PASSWORD  = _env(
        "AZURE_BILLING_DB_PASSWORD",
        legacy="AZURE_BILLING_DB_PASS",
    )

    # --- SSH Tunnel ---
    SSH_HOST     = _env("SSH_HOST")
    SSH_PORT     = _env("SSH_PORT", default="22")
    SSH_USERNAME = _env("SSH_USERNAME", legacy="SSH_USER")
    SSH_PASSWORD = _env("SSH_PASSWORD", legacy="SSH_PASS")
    AZURE_BILLING_SSH_HOST     = os.getenv("AZURE_BILLING_SSH_HOST")
    AZURE_BILLING_SSH_PORT     = os.getenv("AZURE_BILLING_SSH_PORT")
    AZURE_BILLING_SSH_USERNAME = _env("AZURE_BILLING_SSH_USERNAME", legacy="AZURE_BILLING_SSH_USER")
    AZURE_BILLING_SSH_PASSWORD = os.getenv("AZURE_BILLING_SSH_PASSWORD")

    # --- Gemini / LLM ---
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_COMPLEX  = os.getenv("MODEL_COMPLEX")
    MODEL_FAST     = os.getenv("MODEL_FAST")
    MODEL_NANO    = os.getenv("MODEL_NANO")

    # --- Application ---
    APP_ENV     = os.getenv("APP_ENV", "development")
    APP_PORT    = os.getenv("APP_PORT", "3000")
    APP_BASE_URL = os.getenv("APP_BASE_URL")
    LOG_LEVEL   = os.getenv("LOG_LEVEL", "info")

    # --- Feature flags & tunables ---
    FEATURE_USE_FALLBACK_EMBEDDING = os.getenv("FEATURE_USE_FALLBACK_EMBEDDING", "false")
    FEATURE_ENABLE_CLUSTERING      = os.getenv("FEATURE_ENABLE_CLUSTERING", "false")
    LLM_MAX_RETRIES                = os.getenv("LLM_MAX_RETRIES", "3")
    FINANCIAL_QUERY_TIMEOUT_SECONDS = os.getenv("FINANCIAL_QUERY_TIMEOUT_SECONDS", "30")
    MIN_SIGNALS_THRESHOLD          = os.getenv("MIN_SIGNALS_THRESHOLD")
    NEWS_DEBUG_STOP_AFTER_WAVE_2   = os.getenv("NEWS_DEBUG_STOP_AFTER_WAVE_2", "false")
    CLUSTER_CONFIG                 = os.getenv("CLUSTER_CONFIG")
    CLUSTER_INTERPRET_MODEL        = os.getenv("CLUSTER_INTERPRET_MODEL")

    # --- Legacy / optional (not in schema; may be removed) ---
    SLACK_TOKEN   = os.getenv("SLACK_BOT_TOKEN")
    MS_CLIENT_ID     = os.getenv("MS_CLIENT_ID")
    MS_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
    MS_TENANT_ID     = os.getenv("MS_TENANT_ID")
