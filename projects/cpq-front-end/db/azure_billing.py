"""
Azure Billing PostgreSQL client for CPQ profitability.

SSH tunnel: SSH_HOST:SSH_PORT → localhost:5432
(The Azure billing PostgreSQL runs on the SSH server itself, not at db1.peer1.com.)
Shares SSH credentials with Fusion but uses a different remote_bind_address.
"""

import logging
import os
from calendar import monthrange
from datetime import date

import psycopg2
from psycopg2.extras import RealDictCursor
from sshtunnel import SSHTunnelForwarder

MANAGEMENT_FEE_PRODUCT_CODES = ["5799", "5801", "5803"]
logger = logging.getLogger(__name__)

_SSH_HOST = os.environ.get("SSH_HOST", "10.121.21.20")
_SSH_PORT = int(os.environ.get("SSH_PORT", "22"))
_SSH_USER = os.environ.get("SSH_USER", "")
_SSH_PASS = os.environ.get("SSH_PASS", "")

# In prod: set AZURE_BILLING_DB_HOST to the DB server's internal IP (e.g. 10.121.21.20)
# and leave SSH_USER/SSH_PASS unset — the tunnel is skipped and we connect directly.
_AZURE_DB_HOST = os.environ.get("AZURE_BILLING_DB_HOST", "")
_AZURE_DB_PORT = int(os.environ.get("AZURE_BILLING_DB_PORT", "5432"))
_AZURE_DB_NAME = os.environ.get("AZURE_BILLING_DB_NAME", "")
_AZURE_DB_USER = os.environ.get("AZURE_BILLING_DB_USER", "")
_AZURE_DB_PASS = os.environ.get("AZURE_BILLING_DB_PASS", "")

_USE_TUNNEL = bool(_SSH_USER and _SSH_PASS)

_tunnel = None
_conn = None


def _configured() -> bool:
    return bool(_AZURE_DB_NAME and _AZURE_DB_USER and (_USE_TUNNEL or _AZURE_DB_HOST))


def _get_conn():
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
                (_SSH_HOST, _SSH_PORT),
                ssh_username=_SSH_USER,
                ssh_password=_SSH_PASS,
                remote_bind_address=("localhost", _AZURE_DB_PORT),
            )
            _tunnel.start()
            logger.info("azure_billing: SSH tunnel up on localhost:%s", _tunnel.local_bind_port)
        db_host = "localhost"
        db_port = _tunnel.local_bind_port
    else:
        db_host = _AZURE_DB_HOST
        db_port = _AZURE_DB_PORT

    _conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=_AZURE_DB_NAME,
        user=_AZURE_DB_USER,
        password=_AZURE_DB_PASS,
        gssencmode="disable",
        cursor_factory=RealDictCursor,
    )
    _conn.set_session(readonly=True, autocommit=True)
    return _conn


def _billing_period() -> tuple[str, str]:
    """Return (start_date, end_date) for the last complete calendar month."""
    today = date.today()
    year, month = (today.year - 1, 12) if today.month == 1 else (today.year, today.month - 1)
    next_y, next_m = (year + 1, 1) if month == 12 else (year, month + 1)
    return f"{year:04d}-{month:02d}-01", f"{next_y:04d}-{next_m:02d}-01"


def _resolve_customer_ids(conn, ocean_id: int) -> tuple[list[int], list[str]]:
    """Resolve aptum_ids and billing provider UUIDs for an ocean client_id."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id FROM aptum_customer WHERE ocean_client_id = %s",
            (ocean_id,),
        )
        aptum_ids = [r["id"] for r in cur.fetchall() if r.get("id") is not None]

    if not aptum_ids:
        return [], []

    with conn.cursor() as cur:
        cur.execute(
            "SELECT identifier FROM billing_provider_account WHERE aptum_customer_id = ANY(%s::int[])",
            (aptum_ids,),
        )
        customer_ids = [str(r["identifier"]).strip() for r in cur.fetchall() if r.get("identifier") is not None]

    return aptum_ids, customer_ids


def get_cloud_billing_batch(ocean_ids: list[int]) -> dict[int, dict]:
    """
    Fetch last-complete-month billing summary for a list of ocean client IDs.

    Returns dict keyed by ocean_id:
      management_fee_revenue  – sum of customer_invoice_line_item for product codes 5799/5801/5803
      consumption_revenue     – sum of usage_report.retail_pre_tax_total
      consumption_cost        – sum of usage_report.billing_pre_tax_total (Aptum's cost to Microsoft)
      currency                – billing currency
      billing_period_label    – "YYYY-MM"
    """
    if not _configured() or not ocean_ids:
        return {}
    try:
        conn = _get_conn()
        start_date, end_date = _billing_period()
        period_label = start_date[:7]
        result: dict[int, dict] = {}

        for ocean_id in ocean_ids:
            aptum_ids, customer_ids = _resolve_customer_ids(conn, ocean_id)
            if not aptum_ids:
                continue

            currency = "CAD"
            mgmt_revenue = 0.0
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT ci.currency,
                           COALESCE(SUM(cili.total), 0) AS total
                    FROM customer_invoice_line_item cili
                    JOIN customer_invoice ci ON cili.customer_invoice_id = ci.id
                    WHERE ci.aptum_customer_id = ANY(%s::int[])
                      AND cili.charge_start_date >= %s
                      AND cili.charge_start_date  < %s
                      AND cili.product_code = ANY(%s)
                    GROUP BY ci.currency
                    ORDER BY SUM(cili.total) DESC
                    LIMIT 1
                """, (aptum_ids, start_date, end_date, MANAGEMENT_FEE_PRODUCT_CODES))
                row = cur.fetchone()
                if row:
                    mgmt_revenue = float(row["total"] or 0)
                    currency = row["currency"] or "CAD"

            consumption_revenue = 0.0
            consumption_cost = 0.0
            if customer_ids:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT billing_currency AS currency,
                               COALESCE(SUM(retail_pre_tax_total), 0)  AS customer_price,
                               COALESCE(SUM(billing_pre_tax_total), 0) AS provider_cost
                        FROM usage_report
                        WHERE customer_id::text = ANY(%s::text[])
                          AND charge_start_date >= %s
                          AND charge_start_date  < %s
                          AND billing_pre_tax_total > 0
                        GROUP BY billing_currency
                        ORDER BY SUM(retail_pre_tax_total) DESC
                        LIMIT 1
                    """, (customer_ids, start_date, end_date))
                    row = cur.fetchone()
                    if row:
                        consumption_revenue = float(row["customer_price"] or 0)
                        consumption_cost = float(row["provider_cost"] or 0)
                        currency = row["currency"] or currency

            result[ocean_id] = {
                "management_fee_revenue": round(mgmt_revenue, 2),
                "consumption_revenue": round(consumption_revenue, 2),
                "consumption_cost": round(consumption_cost, 2),
                "currency": currency,
                "billing_period_label": period_label,
            }

        return result
    except Exception:
        logger.exception("get_cloud_billing_batch: error")
        return {}


def get_cloud_billing_detail(ocean_id: int) -> dict:
    """
    Full Azure billing breakdown for a single ocean client ID (for the detail page sidebar).

    Returns:
      billing_period_label  – "YYYY-MM"
      management_fees       – list of {fee_code, fee_name, subscription_name, customer_price, currency}
      consumption           – list of {subscription_id, meter_category, customer_price, provider_cost, currency}
      totals                – {management_fee_revenue, consumption_revenue, consumption_cost,
                               total_revenue, total_cost, margin, currency}
    """
    if not _configured():
        return {}
    try:
        conn = _get_conn()
        start_date, end_date = _billing_period()
        period_label = start_date[:7]

        aptum_ids, customer_ids = _resolve_customer_ids(conn, ocean_id)
        if not aptum_ids:
            return {
                "billing_period_label": period_label,
                "management_fees": [],
                "consumption": [],
                "totals": {},
            }

        mgmt_fees = []
        with conn.cursor() as cur:
            cur.execute("""
                SELECT cili.product_code      AS fee_code,
                       cili.description       AS fee_name,
                       cili.description_extra AS subscription_name,
                       COALESCE(cili.total, 0) AS customer_price,
                       ci.currency
                FROM customer_invoice_line_item cili
                JOIN customer_invoice ci ON cili.customer_invoice_id = ci.id
                WHERE ci.aptum_customer_id = ANY(%s::int[])
                  AND cili.charge_start_date >= %s
                  AND cili.charge_start_date  < %s
                  AND cili.product_code = ANY(%s)
                ORDER BY cili.product_code, cili.description_extra
            """, (aptum_ids, start_date, end_date, MANAGEMENT_FEE_PRODUCT_CODES))
            mgmt_fees = [
                {**dict(r), "customer_price": float(r.get("customer_price") or 0)}
                for r in cur.fetchall()
            ]

        consumption = []
        if customer_ids:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT subscription_id,
                           meter_category,
                           billing_currency AS currency,
                           ROUND(SUM(retail_pre_tax_total)::numeric, 2)  AS customer_price,
                           ROUND(SUM(billing_pre_tax_total)::numeric, 2) AS provider_cost
                    FROM usage_report
                    WHERE customer_id::text = ANY(%s::text[])
                      AND charge_start_date >= %s
                      AND charge_start_date  < %s
                      AND billing_pre_tax_total > 0
                    GROUP BY subscription_id, meter_category, billing_currency
                    ORDER BY SUM(retail_pre_tax_total) DESC
                """, (customer_ids, start_date, end_date))
                consumption = [
                    {
                        **dict(r),
                        "customer_price": float(r.get("customer_price") or 0),
                        "provider_cost": float(r.get("provider_cost") or 0),
                        "subscription_id": str(r.get("subscription_id") or ""),
                    }
                    for r in cur.fetchall()
                ]

        mgmt_total = sum(r["customer_price"] for r in mgmt_fees)
        cons_revenue = sum(r["customer_price"] for r in consumption)
        cons_cost = sum(r["provider_cost"] for r in consumption)
        currency = (
            mgmt_fees[0]["currency"] if mgmt_fees
            else consumption[0]["currency"] if consumption
            else "CAD"
        )

        return {
            "billing_period_label": period_label,
            "management_fees": mgmt_fees,
            "consumption": consumption,
            "totals": {
                "management_fee_revenue": round(mgmt_total, 2),
                "consumption_revenue": round(cons_revenue, 2),
                "consumption_cost": round(cons_cost, 2),
                "total_revenue": round(mgmt_total + cons_revenue, 2),
                "total_cost": round(cons_cost, 2),
                "margin": round(mgmt_total + cons_revenue - cons_cost, 2),
                "currency": currency,
            },
        }
    except Exception:
        logger.exception("get_cloud_billing_detail: error")
        return {}
