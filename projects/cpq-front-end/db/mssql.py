import os

MSSQL_SERVER   = os.environ.get("MSSQL_BI_SERVER") or os.environ.get("OCEAN_DB_SERVER", "")
MSSQL_DB       = os.environ.get("MSSQL_BI_NAME")   or os.environ.get("OCEAN_DB_NAME", "")
MSSQL_USER     = os.environ.get("MSSQL_BI_USER")   or os.environ.get("OCEAN_DB_USERNAME", "")
MSSQL_PASSWORD = os.environ.get("MSSQL_BI_PASS")   or os.environ.get("OCEAN_DB_PASSWORD", "")

_HW_SKU_TYPES = {"HW", "Hardware", "hw", "hardware"}


def _connect():
    import pymssql
    return pymssql.connect(
        server=MSSQL_SERVER, user=MSSQL_USER,
        password=MSSQL_PASSWORD, database=MSSQL_DB,
        tds_version="7.0",
    )


def _configured() -> bool:
    return all([MSSQL_SERVER, MSSQL_DB, MSSQL_USER, MSSQL_PASSWORD])


def get_mssql_costs(sku_ids: list[int], sku_level: str) -> dict[int, dict]:
    if not sku_ids or not _configured():
        return {}
    try:
        conn = _connect()
        cur = conn.cursor(as_dict=True)
        placeholders = ",".join(["%d"] * len(sku_ids))
        cur.execute(
            f"SELECT sku_id, sku_name, sku_cost, cost_currency, sku_type, sku_category "
            f"FROM profitability.ocean_sku_cost "
            f"WHERE sku_level = %s AND sku_id IN ({placeholders})",
            (sku_level, *sku_ids),
        )
        result = {}
        for r in cur.fetchall():
            raw_type = (r.get("sku_type") or "").strip()
            is_hw = raw_type in _HW_SKU_TYPES or raw_type.upper().startswith("HW")
            result[r["sku_id"]] = {
                "cost": float(r["sku_cost"] or 0),
                "currency": r["cost_currency"] or "USD",
                "name": r["sku_name"] or "",
                "sku_type": raw_type,
                "sku_category": (r.get("sku_category") or "").strip(),
                "cost_kind": "hw" if is_hw else "sw",
            }
        cur.close()
        conn.close()
        return result
    except Exception:
        return {}


def get_mssql_watts(fusion_id: int) -> int | None:
    if not _configured():
        return None
    try:
        conn = _connect()
        cur = conn.cursor(as_dict=True)
        cur.execute(
            "SELECT watts FROM profitability.hardware_watts WHERE fusion_id = %d",
            (fusion_id,),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row and row.get("watts") is not None:
            return int(row["watts"])
    except Exception:
        pass
    return None


def get_fx_rate(from_currency: str, to_currency: str) -> float:
    if from_currency == to_currency:
        return 1.0
    if not _configured():
        return 1.0
    try:
        conn = _connect()
        cur = conn.cursor(as_dict=True)
        cur.execute(
            "SELECT TOP 1 exchange_rate FROM dbo.dimCurrencyExchangeRates "
            "WHERE from_currency = %s AND to_currency = %s "
            "ORDER BY start_date DESC",
            (from_currency, to_currency),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row and row.get("exchange_rate"):
            return float(row["exchange_rate"])
    except Exception:
        pass
    return 1.0
