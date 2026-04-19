"""
Fusion PostgreSQL (read-only) via SSH tunnel.

Smoke test:
    cd projects/ops-agent && python3 -m ops_agent.fusion

Requires: SSH_HOST, SSH_PORT, SSH_USER, SSH_PASS, FUSION_DB_* in connected-brain/.env
(SSH_USERNAME / SSH_PASSWORD still accepted via settings aliases).
"""

from __future__ import annotations

import logging
import sys

from .config import settings

log = logging.getLogger(__name__)


def smoke() -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    import warnings

    warnings.filterwarnings(
        "ignore",
        message=".*TripleDES.*",
        category=DeprecationWarning,
    )

    try:
        import psycopg2
        from sshtunnel import SSHTunnelForwarder
    except ImportError as e:
        log.error("Missing dependency: %s — pip install psycopg2-binary sshtunnel", e)
        return 1

    host = settings.fusion_db_server
    port = settings.fusion_db_port
    dbname = settings.fusion_db_name
    dbuser = settings.fusion_db_user
    dbpass = settings.fusion_db_pass
    ssh_host = settings.ssh_host
    ssh_port = settings.ssh_port
    ssh_user = settings.ssh_user
    ssh_pass = settings.ssh_pass

    missing = [
        label
        for label, val in (
            ("FUSION_DB_SERVER", host),
            ("FUSION_DB_NAME", dbname),
            ("FUSION_DB_USER", dbuser),
            ("FUSION_DB_PASS", dbpass),
            ("SSH_HOST", ssh_host),
            ("SSH_USER (or SSH_USERNAME)", ssh_user),
            ("SSH_PASS (or SSH_PASSWORD)", ssh_pass),
        )
        if not val
    ]
    if missing:
        log.error("Missing settings: %s", ", ".join(missing))
        return 1

    log.info(
        "Opening SSH tunnel %s@%s:%s → %s:%s …",
        ssh_user,
        ssh_host,
        ssh_port,
        host,
        port,
    )

    try:
        with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_pass,
            remote_bind_address=(host, port),
        ) as tunnel:
            local_port = tunnel.local_bind_port
            log.info("Tunnel up — local port %s", local_port)

            conn = psycopg2.connect(
                host="127.0.0.1",
                port=local_port,
                dbname=dbname,
                user=dbuser,
                password=dbpass,
                gssencmode="disable",
            )
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT current_database(), current_user, inet_server_addr(), inet_server_port()"
                    )
                    row = cur.fetchone()
                    log.info(
                        "Connected: db=%s user=%s server_addr=%s server_port=%s",
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                    )
                    cur.execute("SELECT version()")
                    ver = cur.fetchone()[0]
                    log.info("PostgreSQL: %s", (ver or "").split("\n")[0][:120])

                    cur.execute(
                        """
                        SELECT COUNT(*)::bigint
                        FROM information_schema.tables
                        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                        """
                    )
                    table_count = cur.fetchone()[0]
                    log.info("public base tables: %s", table_count)
            finally:
                conn.close()
    except Exception as e:
        log.error("Fusion smoke failed: %s: %s", type(e).__name__, e)
        return 1

    log.info("Fusion DB smoke test PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(smoke())
