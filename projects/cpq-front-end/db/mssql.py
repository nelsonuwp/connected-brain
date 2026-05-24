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


def _parse_date(value) -> str | None:
    """Normalize a date/datetime from pymssql to 'YYYY-MM-DD' string or None.

    pymssql returns datetime2 columns as strings like '2025-01-08 23:00:00.0000000'
    rather than datetime objects, so we handle both forms.
    Sentinel dates <= 1900-01-01 are normalized to None.
    """
    if value is None:
        return None
    if isinstance(value, str):
        date_str = value[:10]
        return date_str if date_str > "1900-01-01" else None
    if hasattr(value, "date"):
        return value.date().isoformat() if value.year > 1900 else None
    return None


def get_renewal_services(
    company: str | None = None,
    client_id: int | None = None,
    service_id: int | None = None,
    m2m_only: bool = False,
    termed_only: bool = False,
) -> list[dict]:
    """
    Returns services from ocean_services_renewal_date JOIN dimServices.
    Sorted: real future dates first (ascending), then m2m/sentinel dates.
    Expiration dates of 1899-12-31 are normalized to None.
    """
    if not _configured():
        return []
    try:
        conn = _connect()
        cur = conn.cursor(as_dict=True)

        conditions = []
        params = []
        if company:
            conditions.append("osrd.company_name LIKE %s")
            params.append(f"%{company}%")
        if client_id is not None:
            conditions.append("osrd.client_id = %d")
            params.append(int(client_id))
        if service_id is not None:
            conditions.append("osrd.service_id = %d")
            params.append(int(service_id))
        if m2m_only:
            conditions.append("osrd.m2m = 'yes'")
        if termed_only:
            conditions.append("(osrd.m2m IS NULL OR osrd.m2m != 'yes')")

        where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
        sql = f"""
            SELECT
                osrd.client_id, osrd.company_name, osrd.service_id,
                osrd.expiration_date, osrd.m2m,
                ds.product, ds.datacenter_code, ds.currency,
                ds.mrc, ds.provision_date, ds.contract_months_remaining,
                ds.service_type, ds.fusion_id, ds.nickname,
                ds.service_status
            FROM DM_BusinessInsights.renewals.ocean_services_renewal_date osrd
            JOIN DM_BusinessInsights.dbo.dimServices ds
              ON ds.service_id = osrd.service_id
            {where}
            ORDER BY
                CASE
                    WHEN osrd.expiration_date > '1900-01-01'
                         AND (osrd.m2m IS NULL OR osrd.m2m != 'yes')
                    THEN 0 ELSE 1
                END,
                osrd.expiration_date ASC
        """
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)

        rows = cur.fetchall()
        cur.close()
        conn.close()

        result = []
        for r in rows:
            row = dict(r)
            row["expiration_date"] = _parse_date(row.get("expiration_date"))
            row["provision_date"] = _parse_date(row.get("provision_date"))
            row["m2m"] = row.get("m2m") == "yes"
            row["mrc"] = float(row.get("mrc") or 0)
            result.append(row)
        return result
    except Exception:
        return []


def get_service(service_id: int) -> dict | None:
    """Returns one dimServices row for service_id, or None."""
    if not _configured():
        return None
    try:
        conn = _connect()
        cur = conn.cursor(as_dict=True)
        cur.execute(
            "SELECT * FROM DM_BusinessInsights.dbo.dimServices WHERE service_id = %d",
            (service_id,),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            return None
        row = dict(row)
        for k in ("provision_date", "last_updated"):
            row[k] = _parse_date(row.get(k))
        row["mrc"] = float(row.get("mrc") or 0)
        row["usd_mrc"] = float(row.get("usd_mrc") or 0)
        row["cad_mrc"] = float(row.get("cad_mrc") or 0)
        return row
    except Exception:
        return None


def get_service_components(service_id: int) -> list[dict]:
    """Returns all dimComponents rows for service_id, ordered by category/type."""
    if not _configured():
        return []
    try:
        conn = _connect()
        cur = conn.cursor(as_dict=True)
        cur.execute("""
            SELECT
                integer_key, client_id, component_category, service_option_type,
                component_type, component, add_on, currency,
                component_mrc, product_mrc, component_id,
                is_online, service_id, datacenter_code, line_of_business
            FROM DM_BusinessInsights.dbo.dimComponents
            WHERE service_id = %d
            ORDER BY component_category, component_type, component
        """, (service_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        result = []
        for r in rows:
            row = dict(r)
            row["component_mrc"] = float(row.get("component_mrc") or 0)
            row["product_mrc"] = float(row.get("product_mrc") or 0)
            result.append(row)
        return result
    except Exception:
        return []
