"""
MSSQL connector using pymssql via SQLAlchemy.

Env vars (from .env), preferred names:
  MSSQL_BI_SERVER, MSSQL_BI_NAME, MSSQL_BI_USER, MSSQL_BI_PASS

Legacy (still accepted when env_prefix is OCEAN):
  OCEAN_DB_SERVER, OCEAN_DB_NAME, OCEAN_DB_USERNAME, OCEAN_DB_PASSWORD

Uses creator= instead of a URI string so the backslash in domain
usernames (CORP\\user) is never URL-encoded by urllib.
"""

import os

import pymssql
from sqlalchemy import create_engine, text

from .base import BaseConnector


def _read_bi_credentials(prefix: str) -> tuple[str, str, str, str]:
    """Prefer MSSQL_BI_*; fall back to legacy OCEAN_DB_* when prefix is OCEAN."""
    if str(prefix).upper() == "OCEAN":
        server = os.getenv("MSSQL_BI_SERVER") or os.getenv("OCEAN_DB_SERVER", "")
        db = os.getenv("MSSQL_BI_NAME") or os.getenv("OCEAN_DB_NAME", "")
        user = os.getenv("MSSQL_BI_USER") or os.getenv("OCEAN_DB_USERNAME", "")
        password = os.getenv("MSSQL_BI_PASS") or os.getenv("OCEAN_DB_PASSWORD", "")
        return server, db, user, password
    user = os.getenv(f"{prefix}_DB_USERNAME", "")
    password = os.getenv(f"{prefix}_DB_PASSWORD", "")
    server = os.getenv(f"{prefix}_DB_SERVER", "")
    db = os.getenv(f"{prefix}_DB_NAME", "")
    return server, db, user, password


class MSSQLConnector(BaseConnector):
    def __init__(self, config: dict):
        prefix = config.get("env_prefix", "OCEAN")

        server, db, user, password = _read_bi_credentials(prefix)

        missing = [k for k, v in {
            "MSSQL_BI_SERVER or OCEAN_DB_SERVER": server,
            "MSSQL_BI_NAME or OCEAN_DB_NAME": db,
            "MSSQL_BI_USER or OCEAN_DB_USERNAME": user,
            "MSSQL_BI_PASS or OCEAN_DB_PASSWORD": password,
        }.items() if not v]

        if missing:
            raise RuntimeError(f"Missing env vars: {', '.join(missing)}")

        _user, _password, _server, _db = user, password, server, db

        def creator():
            return pymssql.connect(
                server=_server,
                user=_user,
                password=_password,
                database=_db,
            )

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