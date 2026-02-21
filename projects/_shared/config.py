# projects/_shared/config.py
from pathlib import Path
from dotenv import load_dotenv
import os

# Always load from the root, regardless of where the script runs from
root = Path(__file__).parent.parent.parent  # up to ~/connected-brain/
load_dotenv(root / ".env")

class Config:
    # Jira
    JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
    JIRA_EMAIL    = os.getenv("JIRA_EMAIL")
    JIRA_TOKEN    = os.getenv("JIRA_API_TOKEN")

    # Database
    DB_HOST       = os.getenv("DB_HOST")
    DB_PORT       = os.getenv("DB_PORT", "5432")
    DB_NAME       = os.getenv("DB_NAME")
    DB_USER       = os.getenv("DB_USER")
    DB_PASSWORD   = os.getenv("DB_PASSWORD")

    # Slack
    SLACK_TOKEN   = os.getenv("SLACK_BOT_TOKEN")

    # Microsoft Graph
    MS_CLIENT_ID     = os.getenv("MS_CLIENT_ID")
    MS_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
    MS_TENANT_ID     = os.getenv("MS_TENANT_ID")