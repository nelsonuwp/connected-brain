"""
MSSQL connector using pymssql via SQLAlchemy.

Matches oceanClient.get_db_engine() exactly — same env vars and URI pattern.

Env vars (from .env):
  OCEAN_DB_USER      (or OCEAN_DB_USERNAME for backwards compat; fallback: DB_USER)
  OCEAN_DB_PASSWORD  (fallback: DB_PASSWORD)
  OCEAN_DB_SERVER    (fallback: DB_SERVER)
  OCEAN_DB_NAME      (fallback: DB_NAME)

URI: mssql+pymssql://{quote_plus(user)}:{quote_plus(pw)}@{server}/{db}
"""

import os
import urllib.parse

from sqlalchemy import create_engine, text

from .base import BaseConnector


class MSSQLConnector(BaseConnector):
    def __init__(self, config: dict):
        prefix = config.get("env_prefix", "OCEAN")

        # Same env var pattern as oceanClient.get_db_engine()
        user = (
            os.getenv(f"{prefix}_DB_USER")
            or os.getenv(f"{prefix}_DB_USERNAME")
            or os.getenv("DB_USER", "")
        )
        pw = os.getenv(f"{prefix}_DB_PASSWORD") or os.getenv("DB_PASSWORD", "")
        server = os.getenv(f"{prefix}_DB_SERVER") or os.getenv("DB_SERVER", "")
        db = os.getenv(f"{prefix}_DB_NAME") or os.getenv("DB_NAME", "")

        missing = []
        if not user:
            missing.append(f"{prefix}_DB_USER or {prefix}_DB_USERNAME")
        if not server:
            missing.append(f"{prefix}_DB_SERVER")
        if not db:
            missing.append(f"{prefix}_DB_NAME")
        if missing:
            raise RuntimeError(f"Missing env vars: {', '.join(missing)}")

        # Identical to oceanClient: quote_plus + URI, no port (default 1433)
        user_enc = urllib.parse.quote_plus(user)
        pw_enc = urllib.parse.quote_plus(pw)
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
