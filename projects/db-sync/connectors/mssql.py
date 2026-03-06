"""
MSSQL connector using pymssql via SQLAlchemy.

Env vars (from .env):
  OCEAN_DB_USERNAME   (supports domain usernames like CORP\\user)
  OCEAN_DB_PASSWORD
  OCEAN_DB_SERVER
  OCEAN_DB_NAME

Uses creator= instead of a URI string so the backslash in domain
usernames (CORP\\user) is never URL-encoded by urllib.
"""

import os
import json
import time

import pymssql
from sqlalchemy import create_engine, text

from .base import BaseConnector


# region agent log helper
_DEBUG_LOG_PATH = "/Users/anelson-macbook-air/connected-brain/.cursor/debug-4ea72c.log"


def _agent_debug_log(hypothesis_id, message, data=None, run_id="pre-fix"):
    try:
        payload = {
            "sessionId": "4ea72c",
            "runId": run_id,
            "hypothesisId": str(hypothesis_id),
            "location": "projects/db-sync/connectors/mssql.py",
            "message": str(message),
            "data": data or {},
            "timestamp": int(time.time() * 1000),
        }
        with open(_DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
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

        # Pass credentials directly to pymssql — do NOT build a URI string.
        # urllib.quote_plus would encode CORP\\user as CORP%5Cuser, breaking
        # domain authentication entirely.
        _user, _password, _server, _db = user, password, server, db

        def creator():
            # region agent log
            _agent_debug_log(
                "H2",
                "MSSQLConnector creator() connecting",
                {
                    "server": _server,
                    "db": _db,
                    "user_present": bool(_user),
                },
            )
            # endregion
            try:
                conn = pymssql.connect(
                    server=_server,
                    user=_user,
                    password=_password,
                    database=_db,
                )
                # region agent log
                _agent_debug_log(
                    "H2",
                    "MSSQLConnector creator() connected",
                    {"server": _server, "db": _db},
                )
                # endregion
                return conn
            except Exception as e:
                # region agent log
                _agent_debug_log(
                    "H2",
                    "MSSQLConnector creator() connect failed",
                    {
                        "error_type": type(e).__name__,
                        "error": str(e),
                    },
                )
                # endregion
                raise

        self._engine = create_engine("mssql+pymssql://", creator=creator)

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