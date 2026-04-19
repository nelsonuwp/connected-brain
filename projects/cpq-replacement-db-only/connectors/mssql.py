"""
mssql.py — standalone MSSQL connector (no base class dependency)
-----------------------------------------------------------------
Copy this file into any project's connectors/ folder. No other internal
imports required — just pymssql, sqlalchemy, and os.

Env vars (from .env):
    For prefix OCEAN: prefer MSSQL_BI_SERVER, MSSQL_BI_NAME, MSSQL_BI_USER, MSSQL_BI_PASS
    (legacy OCEAN_DB_* still accepted). Other prefixes use {PREFIX}_DB_*.

Usage:
    connector = MSSQLConnector("OCEAN")
    with connector._engine.connect() as conn:
        result = conn.execute(text("SELECT TOP 5 * FROM dbo.MyTable"))
    connector.close()
"""

import os
import pymssql
from sqlalchemy import create_engine


class MSSQLConnector:
    def __init__(self, env_prefix: str = "OCEAN"):
        if str(env_prefix).upper() == "OCEAN":
            server = os.getenv("MSSQL_BI_SERVER") or os.getenv("OCEAN_DB_SERVER", "")
            db = os.getenv("MSSQL_BI_NAME") or os.getenv("OCEAN_DB_NAME", "")
            user = os.getenv("MSSQL_BI_USER") or os.getenv("OCEAN_DB_USERNAME", "")
            password = os.getenv("MSSQL_BI_PASS") or os.getenv("OCEAN_DB_PASSWORD", "")
        else:
            user = os.getenv(f"{env_prefix}_DB_USERNAME", "")
            password = os.getenv(f"{env_prefix}_DB_PASSWORD", "")
            server = os.getenv(f"{env_prefix}_DB_SERVER", "")
            db = os.getenv(f"{env_prefix}_DB_NAME", "")

        if str(env_prefix).upper() == "OCEAN":
            missing_map = {
                "MSSQL_BI_SERVER or OCEAN_DB_SERVER": server,
                "MSSQL_BI_NAME or OCEAN_DB_NAME": db,
                "MSSQL_BI_USER or OCEAN_DB_USERNAME": user,
                "MSSQL_BI_PASS or OCEAN_DB_PASSWORD": password,
            }
        else:
            missing_map = {
                f"{env_prefix}_DB_SERVER": server,
                f"{env_prefix}_DB_NAME": db,
                f"{env_prefix}_DB_USERNAME": user,
                f"{env_prefix}_DB_PASSWORD": password,
            }
        missing = [k for k, v in missing_map.items() if not v]

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

    def close(self):
        self._engine.dispose()