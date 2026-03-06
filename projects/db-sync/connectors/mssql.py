"""
MSSQL connector using pymssql via SQLAlchemy.

Reads env vars matching the actual .env schema:
  OCEAN_DB_SERVER
  OCEAN_DB_NAME
  OCEAN_DB_USERNAME
  OCEAN_DB_PASSWORD

Uses a creator function instead of a URI string so that domain usernames
like CORP\\username pass through to pymssql without being URL-encoded.
"""

import os

import pymssql
from sqlalchemy import create_engine, text

from .base import BaseConnector


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

        # creator bypasses URI parsing — domain usernames like CORP\\user
        # would get mangled by urllib quote_plus if passed as a URI string
        def creator():
            return pymssql.connect(
                server=server,
                user=user,
                password=password,
                database=db,
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