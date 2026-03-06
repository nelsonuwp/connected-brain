"""
MSSQL connector using pymssql via SQLAlchemy.

Env vars (from .env):
  OCEAN_DB_USERNAME   (supports domain usernames like CORP\\user)
  OCEAN_DB_PASSWORD
  OCEAN_DB_SERVER
  OCEAN_DB_NAME

Uses URI with quote_plus so domain usernames (CORP\\user) are passed as
SQL auth, not Windows Integrated auth. Passing user= directly to pymssql
triggers Integrated auth on Mac, causing "untrusted domain" errors.
"""

import os
import json
import time
import urllib.parse
from pathlib import Path

from sqlalchemy import create_engine, text

from .base import BaseConnector


# region agent log helper
def _agent_debug_log(hypothesis_id, message, data=None, run_id="pre-fix"):
    try:
        # Repo root: connectors/mssql.py -> parents[3] = connected-brain
        _log_path = Path(__file__).resolve().parents[3] / ".cursor" / "debug-4ea72c.log"
        _log_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "sessionId": "4ea72c",
            "runId": run_id,
            "hypothesisId": str(hypothesis_id),
            "location": "projects/db-sync/connectors/mssql.py",
            "message": str(message),
            "data": data or {},
            "timestamp": int(time.time() * 1000),
        }
        with open(_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
    except Exception:
        # Swallow logging errors to avoid impacting main flow
        pass


# endregion


class MSSQLConnector(BaseConnector):
    def __init__(self, config: dict):
        prefix = config.get("env_prefix", "OCEAN")

        user     = os.getenv(f"{prefix}_DB_USERNAME", "")
        password = os.getenv(f"{prefix}_DB_PASSWORD", "")
        server   = os.getenv(f"{prefix}_DB_SERVER", "")
        db       = os.getenv(f"{prefix}_DB_NAME", "")

        missing = [k for k, v in {
            f"{prefix}_DB_USERNAME": user,
            f"{prefix}_DB_SERVER":   server,
            f"{prefix}_DB_NAME":     db,
        }.items() if not v]

        if missing:
            raise RuntimeError(f"Missing env vars: {', '.join(missing)}")

        # region agent log
        _agent_debug_log(
            "H1",
            "MSSQLConnector env vars loaded",
            {
                "prefix": prefix,
                "has_user": bool(user),
                "has_password": bool(password),
                "server": server,
                "db": db,
            },
        )
        # endregion

        # Use URI with quote_plus (like oceanClient). Passing user= directly
        # to pymssql.connect() triggers Windows Integrated auth on Mac, causing
        # "Login from untrusted domain" failures. URI + SQL auth works.
        user_enc = urllib.parse.quote_plus(user)
        pw_enc = urllib.parse.quote_plus(password)
        uri = f"mssql+pymssql://{user_enc}:{pw_enc}@{server}/{db}"
        self._engine = create_engine(uri)

    def get_schema(self, entry: dict) -> list[dict]:
        database = entry["database"]
        schema   = entry.get("schema", "dbo")
        table    = entry["table"]

        with self._engine.connect() as conn:
            rows = conn.execute(
                text(f"""
                    SELECT
                        COLUMN_NAME,
                        DATA_TYPE,
                        CHARACTER_MAXIMUM_LENGTH,
                        NUMERIC_PRECISION,
                        NUMERIC_SCALE,
                        IS_NULLABLE
                    FROM [{database}].INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = :schema
                      AND TABLE_NAME   = :table
                    ORDER BY ORDINAL_POSITION
                """),
                {"schema": schema, "table": table},
            ).fetchall()

        fields = []
        for col_name, data_type, char_max, num_prec, num_scale, nullable in rows:
            if char_max:
                type_str = f"{data_type}({'MAX' if char_max == -1 else char_max})"
            elif num_prec and num_scale:
                type_str = f"{data_type}({num_prec},{num_scale})"
            elif num_prec:
                type_str = f"{data_type}({num_prec})"
            else:
                type_str = data_type
            fields.append({
                "name":     col_name,
                "type":     type_str,
                "nullable": nullable,
                "notes":    "",
            })
        return fields

    def get_sample(self, entry: dict, limit: int = 5) -> list[dict]:
        database = entry["database"]
        schema   = entry.get("schema", "dbo")
        table    = entry["table"]

        with self._engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT TOP {limit} * FROM [{database}].[{schema}].[{table}]")
            )
            columns = list(result.keys())
            return [dict(zip(columns, row)) for row in result.fetchall()]

    def close(self):
        self._engine.dispose()