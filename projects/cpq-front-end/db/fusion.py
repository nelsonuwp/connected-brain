import os
from decimal import Decimal

import psycopg2
from psycopg2.extras import RealDictCursor
from sshtunnel import SSHTunnelForwarder

from lib.overhead import COST_DRIVERS

SSH_HOST     = os.environ.get("SSH_HOST", "10.121.21.20")
SSH_PORT     = int(os.environ.get("SSH_PORT", "22"))
SSH_USER     = os.environ.get("SSH_USER", "")
SSH_PASSWORD = os.environ.get("SSH_PASS", "")

DB_REMOTE_HOST = os.environ.get("FUSION_DB_SERVER", "db1.peer1.com")
DB_REMOTE_PORT = int(os.environ.get("FUSION_DB_PORT", "5432"))
DB_NAME        = os.environ.get("FUSION_DB_NAME", "fusion")
DB_USER        = os.environ.get("FUSION_DB_USER", "sb_readonly")
DB_PASSWORD    = os.environ.get("FUSION_DB_PASS", "")

_tunnel = None
_conn   = None
_USE_TUNNEL = bool(SSH_USER and SSH_PASSWORD)

if _USE_TUNNEL:
    print(f"[fusion] SSH tunnel via {SSH_HOST}")
else:
    print("[fusion] direct connection mode")


def get_conn():
    global _tunnel, _conn
    if _conn:
        try:
            _conn.cursor().execute("SELECT 1")
            return _conn
        except Exception:
            _conn = None
    if _USE_TUNNEL:
        if _tunnel and not _tunnel.is_active:
            _tunnel = None
        if not _tunnel:
            _tunnel = SSHTunnelForwarder(
                (SSH_HOST, SSH_PORT),
                ssh_username=SSH_USER,
                ssh_password=SSH_PASSWORD,
                remote_bind_address=(DB_REMOTE_HOST, DB_REMOTE_PORT),
            )
            _tunnel.start()
        db_host = "127.0.0.1"
        db_port = _tunnel.local_bind_port
    else:
        db_host = DB_REMOTE_HOST
        db_port = DB_REMOTE_PORT
    _conn = psycopg2.connect(
        host=db_host, port=db_port,
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
        gssencmode="disable", cursor_factory=RealDictCursor,
    )
    _conn.set_session(readonly=True, autocommit=True)
    return _conn


_dc_registry = None


def _build_registry_from_cost_drivers() -> dict:
    result = {}
    for code, dc in COST_DRIVERS["data_centers"].items():
        native = dc["native_currency"]
        result[code] = {
            "id": dc["fusion_dc_id"], "dc_abbr": code, "name": dc["name"],
            "city": None, "state": None, "currencies": [native], "native_currency": native,
        }
    return result


def get_dc_registry() -> dict:
    global _dc_registry
    if _dc_registry is not None:
        return _dc_registry
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT sd.id, sd.dc_abbr, sd.name, sd.city, sd.state,
                       array_agg(dac.currency_code ORDER BY dac.currency_code)
                         FILTER (WHERE dac.currency_code IS NOT NULL) AS currencies
                FROM public.sb_datacenter sd
                LEFT JOIN public.datacenter_available_currencies dac ON dac.datacenter_id = sd.id
                WHERE sd.active = true
                GROUP BY sd.id, sd.dc_abbr, sd.name, sd.city, sd.state
                ORDER BY sd.dc_abbr
            """)
            rows = cur.fetchall()
        registry = {}
        for r in rows:
            abbr = r["dc_abbr"]
            currencies = r["currencies"] or []
            cd_entry = COST_DRIVERS["data_centers"].get(abbr, {})
            if len(currencies) == 1:
                native = currencies[0]
            else:
                native = cd_entry.get("native_currency") or (currencies[0] if currencies else "USD")
            registry[abbr] = {
                "id": r["id"], "dc_abbr": abbr, "name": r["name"],
                "city": r.get("city"), "state": r.get("state"),
                "currencies": currencies, "native_currency": native,
            }
        _dc_registry = registry
    except Exception:
        _dc_registry = _build_registry_from_cost_drivers()
    return _dc_registry


def get_dc_info(dc_abbr: str) -> dict | None:
    return get_dc_registry().get(dc_abbr.upper())


def dec(v) -> float:
    if v is None:
        return 0.0
    if isinstance(v, Decimal):
        return float(v)
    return float(v)
