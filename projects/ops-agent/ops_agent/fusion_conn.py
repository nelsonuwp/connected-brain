"""
Persistent SSH tunnel + psycopg2 thread pool for Fusion PostgreSQL.

Started from FastAPI lifespan; read-only.
"""

from __future__ import annotations

import logging
import warnings
from typing import Optional

from .config import settings

logger = logging.getLogger(__name__)

_tunnel = None
_pool = None


def fusion_env_ready() -> bool:
    return bool(
        settings.fusion_db_server
        and settings.fusion_db_name
        and settings.fusion_db_user
        and settings.fusion_db_pass
        and settings.ssh_host
        and settings.ssh_user
        and settings.ssh_pass
    )


def start_fusion() -> None:
    """Open SSH tunnel and connection pool. No-op if env incomplete."""
    global _tunnel, _pool  # noqa: PLW0603

    if not fusion_env_ready():
        logger.warning("Fusion credentials or SSH not configured — Fusion features disabled")
        return

    # Paramiko / cryptography deprecation noise on import
    warnings.filterwarnings(
        "ignore",
        message=".*TripleDES.*",
        category=DeprecationWarning,
    )

    from psycopg2.pool import ThreadedConnectionPool
    from sshtunnel import SSHTunnelForwarder

    _tunnel = SSHTunnelForwarder(
        (settings.ssh_host, settings.ssh_port),
        ssh_username=settings.ssh_user,
        ssh_password=settings.ssh_pass,
        remote_bind_address=(settings.fusion_db_server, settings.fusion_db_port),
    )
    _tunnel.start()
    local_port = _tunnel.local_bind_port
    logger.info(
        "Fusion SSH tunnel up → local port %s → %s:%s",
        local_port,
        settings.fusion_db_server,
        settings.fusion_db_port,
    )

    _pool = ThreadedConnectionPool(
        minconn=1,
        maxconn=6,
        host="127.0.0.1",
        port=local_port,
        dbname=settings.fusion_db_name,
        user=settings.fusion_db_user,
        password=settings.fusion_db_pass,
        gssencmode="disable",
    )
    logger.info("Fusion connection pool ready")


def stop_fusion() -> None:
    global _pool, _tunnel
    if _pool is not None:
        try:
            _pool.closeall()
        except Exception as e:
            logger.warning("Fusion pool close: %s", e)
        _pool = None
    if _tunnel is not None:
        try:
            _tunnel.stop()
        except Exception as e:
            logger.warning("Fusion tunnel stop: %s", e)
        _tunnel = None


def fusion_pool():
    """Return pool or None if Fusion was not started."""
    return _pool
