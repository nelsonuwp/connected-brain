"""
Read-only MSSQL BI (DM_BusinessInsights) connectivity.

Smoke test:
    cd projects/ops-agent && python3 -m ops_agent.mssql

Requires in connected-brain/.env: MSSQL_BI_SERVER, MSSQL_BI_NAME, MSSQL_BI_USER, MSSQL_BI_PASS
(legacy OCEAN_DB_* still accepted via settings aliases).
"""

from __future__ import annotations

import logging
import sys

import pymssql

from .config import settings

log = logging.getLogger(__name__)


def smoke() -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    server = settings.mssql_bi_server
    database = settings.mssql_bi_name
    user = settings.mssql_bi_user
    password = settings.mssql_bi_pass

    missing = [
        name
        for name, val in (
            ("MSSQL_BI_SERVER (or OCEAN_DB_SERVER)", server),
            ("MSSQL_BI_NAME (or OCEAN_DB_NAME)", database),
            ("MSSQL_BI_USER (or OCEAN_DB_USERNAME)", user),
            ("MSSQL_BI_PASS (or OCEAN_DB_PASSWORD)", password),
        )
        if not val
    ]
    if missing:
        log.error("Missing MSSQL BI settings: %s", ", ".join(missing))
        return 1

    log.info("Connecting to %s / %s as %s …", server, database, user)
    try:
        conn = pymssql.connect(
            server=server,
            user=user,
            password=password,
            database=database,
        )
    except Exception as e:
        log.error("Connection failed: %s: %s", type(e).__name__, e)
        return 1

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT DB_NAME(), USER_NAME(), @@VERSION")
            row = cur.fetchone()
            log.info("DB_NAME=%s  USER=%s", row[0], row[1])
            log.info("Version (first line): %s", (row[2] or "").split("\n")[0][:120])

            cur.execute(
                """
                SELECT COUNT_BIG(*) AS n
                FROM dbo.dimComponents WITH (NOLOCK)
                """
            )
            n = cur.fetchone()[0]
            log.info("dimComponents row count (approx): %s", f"{n:,}")

            cur.execute(
                """
                SELECT TOP 1 service_id, component_id, component_type, component
                FROM dbo.dimComponents WITH (NOLOCK)
                ORDER BY last_updated DESC
                """
            )
            sample = cur.fetchone()
            if sample:
                log.info(
                    "Latest dimComponents sample: service_id=%s component_id=%s type=%s label=%s",
                    sample[0],
                    sample[1],
                    sample[2],
                    (sample[3] or "")[:80],
                )
    finally:
        conn.close()

    log.info("MSSQL BI smoke test PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(smoke())
