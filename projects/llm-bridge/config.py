"""
LLM Bridge config. Loads parent .env then project .env (project wins).
Validates OPENROUTER_API_KEY on import — fails fast if missing.
"""
from pathlib import Path

from dotenv import load_dotenv

# Load parent first, then project overrides
load_dotenv(Path.home() / "connected-brain" / ".env")
load_dotenv(Path(__file__).resolve().parent / ".env", override=True)

# Import after load_dotenv so env vars are available
import os


def _path_default(path_str: str) -> Path:
    return Path(path_str).expanduser()


class Config:
    """Single config dataclass. Paths expanded from ~ at load time."""

    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "").strip()
    VAULT_ROOT: Path = _path_default(os.getenv("VAULT_ROOT", "~/connected-brain/vault"))
    TEMPLATES_ROOT: Path = _path_default(os.getenv("TEMPLATES_ROOT", "~/connected-brain/_templates"))
    PROMPTS_ROOT: Path = _path_default(os.getenv("PROMPTS_ROOT", "~/connected-brain/vault/_prompts"))
    LLM_MAX_RETRIES: int = int(os.getenv("LLM_MAX_RETRIES", "3"))
    MODEL_REASONING: str = os.getenv("MODEL_REASONING", "anthropic/claude-opus-4-5")
    MODEL_WORKHORSE: str = os.getenv("MODEL_WORKHORSE", "anthropic/claude-sonnet-4-5")
    MODEL_NANO: str = os.getenv("MODEL_NANO", "anthropic/claude-haiku-4-5")
    TEMPERATURE_REASONING: float = float(os.getenv("TEMPERATURE_REASONING", "1.0"))
    TEMPERATURE_WORKHORSE: float = float(os.getenv("TEMPERATURE_WORKHORSE", "0.4"))
    TEMPERATURE_NANO: float = float(os.getenv("TEMPERATURE_NANO", "0.3"))


# Fail fast on missing API key
if not Config.OPENROUTER_API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY is not set. Add it to ~/connected-brain/.env"
    )
