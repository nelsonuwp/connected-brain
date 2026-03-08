"""
mssql.py — standalone MSSQL connector (no base class dependency)
-----------------------------------------------------------------
Copy this file into any project's connectors/ folder. No other internal
imports required — just pymssql, sqlalchemy, and os.

Env vars (from .env):
    {PREFIX}_DB_USERNAME   (supports domain usernames like CORP\\user)
    {PREFIX}_DB_PASSWORD
    {PREFIX}_DB_SERVER
    {PREFIX}_DB_NAME

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
        user     = os.getenv(f"{env_prefix}_DB_USERNAME", "")
        password = os.getenv(f"{env_prefix}_DB_PASSWORD", "")
        server   = os.getenv(f"{env_prefix}_DB_SERVER", "")
        db       = os.getenv(f"{env_prefix}_DB_NAME", "")

        missing = [k for k, v in {
            f"{env_prefix}_DB_USERNAME": user,
            f"{env_prefix}_DB_SERVER":   server,
            f"{env_prefix}_DB_NAME":     db,
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

    def close(self):
        self._engine.dispose()