"""
Build T-shaped context for a ticket: customer history + same-hardware neighbors.

MSSQL + Fusion calls run in asyncio.to_thread (sync drivers).
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Optional

import pymssql
from psycopg2.extras import RealDictCursor

from ..config import settings
from ..fusion_conn import fusion_pool
from ..db import (
    get_ticket,
    get_ticket_assets,
    list_customer_tickets,
    list_tickets_for_service_ids,
)
from .semantic import (
    SEMANTIC_LIMIT_CUSTOMER,
    SEMANTIC_LIMIT_NEIGHBOR,
    embed_current_ticket,
    merge_with_recency_fallback,
    similar_customer_tickets,
    similar_neighbor_tickets,
)

logger = logging.getLogger(__name__)

CUSTOMER_TICKET_LIMIT = 30
NEIGHBOR_TICKET_LIMIT = 25
K_NEIGHBOR_CANDIDATES = 50
MIN_SHARED_COMPONENTS = 2
MAX_COMPONENT_IDS_IN = 350
MAX_NEIGHBOR_FOR_JACCARD = 30


def _parse_service_ids(assets: list[dict]) -> list[int]:
    out: list[int] = []
    for a in assets:
        sid = a.get("service_id")
        if sid is None:
            continue
        s = str(sid).strip()
        if not s.isdigit():
            continue
        out.append(int(s))
    return sorted(set(out))


def _mssql_slice(service_ids: list[int]) -> dict[str, Any]:
    """dimComponents fingerprint + neighbor service_ids (ranked by Jaccard)."""
    result: dict[str, Any] = {
        "components": [],
        "neighbor_services": [],
        "mssql_error": None,
    }
    if not settings.mssql_bi_server or not settings.mssql_bi_name:
        result["mssql_error"] = "MSSQL BI not configured"
        return result
    if not service_ids:
        return result

    try:
        conn = pymssql.connect(
            server=settings.mssql_bi_server,
            user=settings.mssql_bi_user,
            password=settings.mssql_bi_pass,
            database=settings.mssql_bi_name,
        )
    except Exception as e:
        result["mssql_error"] = f"{type(e).__name__}: {e}"
        return result

    try:
        cur = conn.cursor()
        ph = ",".join(["%s"] * len(service_ids))
        cur.execute(
            f"""
            SELECT service_id, component_id, component_type, component, component_category, is_online
            FROM dbo.dimComponents WITH (NOLOCK)
            WHERE service_id IN ({ph})
            """,
            tuple(service_ids),
        )
        rows = cur.fetchall()
        source_components: list[dict[str, Any]] = []
        source_cids: set[int] = set()
        for r in rows:
            sid, cid, ctype, comp, cat, online = r[0], r[1], r[2], r[3], r[4], r[5]
            source_components.append(
                {
                    "service_id": sid,
                    "component_id": cid,
                    "component_type": ctype,
                    "component": comp,
                    "component_category": cat,
                    "is_online": online,
                }
            )
            if str(online).strip().lower() in ("yes", "true", "1"):
                source_cids.add(int(cid))
        result["components"] = source_components

        if len(source_cids) > MAX_COMPONENT_IDS_IN:
            # Keep highest-frequency component_ids on ticket services (arbitrary cap)
            source_cids = set(sorted(source_cids)[:MAX_COMPONENT_IDS_IN])

        if not source_cids:
            return result

        cid_list = sorted(source_cids)
        ph_c = ",".join(["%s"] * len(cid_list))
        ph_s = ",".join(["%s"] * len(service_ids))
        cur.execute(
            f"""
            SELECT TOP {K_NEIGHBOR_CANDIDATES} c.service_id,
                   COUNT(DISTINCT c.component_id) AS shared
            FROM dbo.dimComponents c WITH (NOLOCK)
            WHERE c.component_id IN ({ph_c})
              AND c.service_id NOT IN ({ph_s})
              AND c.is_online = 'Yes'
            GROUP BY c.service_id
            HAVING COUNT(DISTINCT c.component_id) >= %s
            ORDER BY shared DESC
            """,
            tuple(cid_list) + tuple(service_ids) + (MIN_SHARED_COMPONENTS,),
        )
        candidates = [(int(r[0]), int(r[1])) for r in cur.fetchall()]
        if not candidates:
            return result

        neighbor_sids = [c[0] for c in candidates[:MAX_NEIGHBOR_FOR_JACCARD]]
        ph_n = ",".join(["%s"] * len(neighbor_sids))
        cur.execute(
            f"""
            SELECT service_id, component_id
            FROM dbo.dimComponents WITH (NOLOCK)
            WHERE service_id IN ({ph_n})
              AND is_online = 'Yes'
            """,
            tuple(neighbor_sids),
        )
        neigh_map: dict[int, set[int]] = {}
        for sid, cid in cur.fetchall():
            neigh_map.setdefault(int(sid), set()).add(int(cid))

        scored: list[tuple[int, float, int]] = []
        for nsid, shared_count in candidates[:MAX_NEIGHBOR_FOR_JACCARD]:
            nset = neigh_map.get(nsid, set())
            inter = len(source_cids & nset)
            union = len(source_cids | nset) or 1
            jaccard = inter / union
            scored.append((nsid, jaccard, shared_count))

        scored.sort(key=lambda x: (-x[1], -x[2]))
        for nsid, jacc, shared in scored[:25]:
            result["neighbor_services"].append(
                {"service_id": nsid, "jaccard": round(jacc, 4), "shared_components": shared}
            )
    finally:
        conn.close()

    return result


def _fusion_slice(client_id: Optional[int], service_ids: list[int]) -> dict[str, Any]:
    out: dict[str, Any] = {
        "customer": None,
        "tam": [],
        "services": [],
        "ticket_services_fusion": [],
        "resolved_client_id": client_id,
        "fusion_error": None,
    }
    pool = fusion_pool()
    if pool is None:
        out["fusion_error"] = "Fusion pool not running"
        return out

    conn = pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            ticket_rows: list[dict] = []
            if service_ids:
                cur.execute(
                    """
                    SELECT id, customers_id, products_name, products_nickname, products_model,
                           products_status_id, mrc, currency
                    FROM customer_products
                    WHERE id = ANY(%s)
                    """,
                    (service_ids,),
                )
                by_id = {int(r["id"]): dict(r) for r in cur.fetchall()}
                for sid in service_ids:
                    if sid in by_id:
                        ticket_rows.append(by_id[sid])
            out["ticket_services_fusion"] = ticket_rows

            resolved = client_id
            if resolved is None and ticket_rows:
                cid0 = ticket_rows[0].get("customers_id")
                if cid0 is not None:
                    resolved = int(cid0)
            out["resolved_client_id"] = resolved

            if resolved is not None:
                cur.execute(
                    """
                    SELECT customers_id, company_name, blacklisted
                    FROM customers
                    WHERE customers_id = %s
                    """,
                    (resolved,),
                )
                row = cur.fetchone()
                if row:
                    out["customer"] = dict(row)

                try:
                    cur.execute(
                        """
                        SELECT e.first_name, e.last_name, e.email_address
                        FROM customer_tam ct
                        JOIN employees e ON e.id = ct.employees_id
                        WHERE ct.customers_id = %s
                        LIMIT 5
                        """,
                        (resolved,),
                    )
                    out["tam"] = [dict(r) for r in cur.fetchall()]
                except Exception as tam_e:
                    logger.warning("customer_tam join failed (non-fatal): %s", tam_e)
                    out["tam"] = []

                cur.execute(
                    """
                    SELECT id, customers_id, products_name, products_nickname, products_model,
                           products_status_id, mrc, currency
                    FROM customer_products
                    WHERE customers_id = %s
                    ORDER BY id DESC
                    LIMIT 80
                    """,
                    (resolved,),
                )
                out["services"] = [dict(r) for r in cur.fetchall()]
    except Exception as e:
        out["fusion_error"] = f"{type(e).__name__}: {e}"
        logger.exception("Fusion slice failed")
    finally:
        pool.putconn(conn)

    return out


def _fusion_service_labels(service_ids: list[int]) -> dict[int, dict[str, Any]]:
    """
    Map Fusion customer_products.id (service PK) → product label + owning customer company.
    """
    out: dict[int, dict[str, Any]] = {}
    if not service_ids:
        return out
    pool = fusion_pool()
    if pool is None:
        return out
    conn = pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT cp.id, cp.products_name, cp.products_nickname, cp.customers_id,
                       c.company_name
                FROM customer_products cp
                JOIN customers c ON c.customers_id = cp.customers_id
                WHERE cp.id = ANY(%s)
                """,
                (service_ids,),
            )
            for r in cur.fetchall():
                sid = int(r["id"])
                name = (r.get("products_name") or "").strip()
                nick = (r.get("products_nickname") or "").strip()
                product_label = name or nick or f"service {sid}"
                out[sid] = {
                    "product_name": name or nick,
                    "product_nickname": nick,
                    "product_label": product_label,
                    "fusion_company_name": (r.get("company_name") or "").strip(),
                    "customers_id": r.get("customers_id"),
                }
    finally:
        pool.putconn(conn)
    return out


def _fusion_company_by_client_ids(client_ids: list[int]) -> dict[int, str]:
    """Map customers_id → company_name for ticket rows."""
    out: dict[int, str] = {}
    if not client_ids:
        return out
    pool = fusion_pool()
    if pool is None:
        return out
    conn = pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT customers_id, company_name
                FROM customers
                WHERE customers_id = ANY(%s)
                """,
                (client_ids,),
            )
            for r in cur.fetchall():
                cid = r.get("customers_id")
                if cid is not None:
                    out[int(cid)] = (r.get("company_name") or "").strip()
    finally:
        pool.putconn(conn)
    return out


def _apply_service_labels(
    components: list[dict[str, Any]],
    neighbor_services: list[dict[str, Any]],
    label_map: dict[int, dict[str, Any]],
) -> None:
    for row in components:
        sid = row.get("service_id")
        if sid is None:
            continue
        info = label_map.get(int(sid))
        if not info:
            continue
        row["product_label"] = info.get("product_label")
        row["fusion_company_name"] = info.get("fusion_company_name")
    for row in neighbor_services:
        sid = row.get("service_id")
        if sid is None:
            continue
        info = label_map.get(int(sid))
        if not info:
            continue
        row["product_label"] = info.get("product_label")
        row["fusion_company_name"] = info.get("fusion_company_name")


def _json_safe(obj: Any) -> Any:
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_json_safe(x) for x in obj]
    return obj


@dataclass
class TContextView:
    """Serializable view for templates + LLM prompts."""

    issue_key: str
    summary: str
    status: str
    client_id: Optional[int]
    customer_name: Optional[str]
    tam_display: Optional[str]
    fusion_error: Optional[str]
    mssql_error: Optional[str]
    customer_tickets: list[dict[str, Any]] = field(default_factory=list)
    components_sample: list[dict[str, Any]] = field(default_factory=list)
    neighbor_services: list[dict[str, Any]] = field(default_factory=list)
    neighbor_tickets: list[dict[str, Any]] = field(default_factory=list)
    ticket_fusion_services: list[dict[str, Any]] = field(default_factory=list)
    fusion_services_for_client: list[dict[str, Any]] = field(default_factory=list)

    def to_template_dict(self) -> dict[str, Any]:
        d = asdict(self)
        return _json_safe(d)

    def prompt_block(self) -> str:
        """Dense text block for LLM user prompts."""
        lines = [
            f"=== TICKET {self.issue_key} ===",
            f"Summary: {self.summary}",
            f"Status: {self.status}",
            f"Customer ID (Ocean/Fusion): {self.client_id or 'unknown'}",
            f"Customer name: {self.customer_name or 'unknown'}",
        ]
        if self.tam_display:
            lines.append(f"Account TAM (Fusion): {self.tam_display}")
        if self.fusion_error:
            lines.append(f"[Fusion note: {self.fusion_error}]")
        if self.mssql_error:
            lines.append(f"[MSSQL note: {self.mssql_error}]")

        lines.append("\n=== CUSTOMER TICKET HISTORY (recent) ===")
        for t in self.customer_tickets[:20]:
            cust = (
                t.get("fusion_company_name")
                or t.get("jira_org_name")
                or (f"client {t.get('ocean_client_id')}" if t.get("ocean_client_id") else "")
            )
            lines.append(
                f"- {t.get('issue_key')} | {t.get('status')} | {cust} | "
                f"{(t.get('summary') or '')[:120]}"
            )

        lines.append("\n=== HARDWARE COMPONENTS (this ticket's services, MSSQL dimComponents) ===")
        for c in self.components_sample[:40]:
            pl = c.get("product_label") or ""
            co = c.get("fusion_company_name") or ""
            extra = f" [{pl}] [{co}]" if (pl or co) else ""
            lines.append(
                f"- svc {c.get('service_id')}{extra} · comp {c.get('component_id')} "
                f"{c.get('component_category')}/{c.get('component_type')}: {c.get('component')}"
            )

        lines.append("\n=== NEIGHBOR SERVICES (shared components / Jaccard) ===")
        for n in self.neighbor_services[:15]:
            pl = n.get("product_label") or ""
            co = n.get("fusion_company_name") or ""
            extra = f" · {pl} · {co}" if (pl or co) else ""
            lines.append(
                f"- service_id {n.get('service_id')}{extra} · "
                f"jaccard={n.get('jaccard')} shared={n.get('shared_components')}"
            )

        lines.append("\n=== TICKETS ON NEIGHBOR SERVICES (any customer) ===")
        for t in self.neighbor_tickets[:20]:
            cust = (
                t.get("fusion_company_name")
                or t.get("jira_org_name")
                or (f"client {t.get('ocean_client_id')}" if t.get("ocean_client_id") else "")
            )
            lines.append(
                f"- {t.get('issue_key')} | {t.get('status')} | {cust} | "
                f"{(t.get('summary') or '')[:100]}"
            )

        return "\n".join(lines)


async def build_t_context(pool, issue_key: str) -> dict[str, Any]:
    async with pool.acquire() as conn:
        ticket = await get_ticket(conn, issue_key)
        if not ticket:
            return {"error": "ticket_not_found", "issue_key": issue_key}

        assets = await get_ticket_assets(conn, issue_key)
        service_ids = _parse_service_ids(assets)

        client_id = ticket.get("ocean_client_id")
        if client_id is not None:
            client_id = int(client_id)

        mssql_data = await asyncio.to_thread(_mssql_slice, service_ids)
        fusion_data = await asyncio.to_thread(_fusion_slice, client_id, service_ids)

        resolved_client = fusion_data.get("resolved_client_id")
        if resolved_client is not None:
            resolved_client = int(resolved_client)
        elif client_id is not None:
            resolved_client = int(client_id)

        customer_tickets: list[dict] = []
        if resolved_client is not None:
            customer_tickets = await list_customer_tickets(
                conn, resolved_client, exclude_issue_key=issue_key, limit=CUSTOMER_TICKET_LIMIT
            )

        neighbor_sids = [n["service_id"] for n in mssql_data.get("neighbor_services") or []]
        neighbor_sid_strs = [str(x) for x in neighbor_sids]
        neighbor_tickets: list[dict] = []
        if neighbor_sid_strs:
            neighbor_tickets = await list_tickets_for_service_ids(
                conn, neighbor_sid_strs, exclude_issue_key=issue_key, limit=NEIGHBOR_TICKET_LIMIT
            )

        # Fusion labels for every service_id appearing in components + neighbors (+ ticket assets)
        label_ids: set[int] = set(service_ids)
        for c in mssql_data.get("components") or []:
            if c.get("service_id") is not None:
                label_ids.add(int(c["service_id"]))
        for n in mssql_data.get("neighbor_services") or []:
            if n.get("service_id") is not None:
                label_ids.add(int(n["service_id"]))
        label_map: dict[int, dict[str, Any]] = {}
        if label_ids and fusion_pool() is not None:
            label_map = await asyncio.to_thread(_fusion_service_labels, sorted(label_ids))

        comps = list(mssql_data.get("components") or [])
        neigh_svcs = list(mssql_data.get("neighbor_services") or [])
        _apply_service_labels(comps, neigh_svcs, label_map)

        # Fusion company for ticket rows (Ocean client id = Fusion customers_id)
        client_label_ids: set[int] = set()
        for trow in neighbor_tickets:
            oc = trow.get("ocean_client_id")
            if oc is not None:
                client_label_ids.add(int(oc))
        for trow in customer_tickets:
            oc = trow.get("ocean_client_id")
            if oc is not None:
                client_label_ids.add(int(oc))
        company_map: dict[int, str] = {}
        if client_label_ids and fusion_pool() is not None:
            company_map = await asyncio.to_thread(
                _fusion_company_by_client_ids, sorted(client_label_ids)
            )
        for trow in neighbor_tickets:
            oc = trow.get("ocean_client_id")
            if oc is not None:
                name = company_map.get(int(oc))
                if name:
                    trow["fusion_company_name"] = name
        for trow in customer_tickets:
            oc = trow.get("ocean_client_id")
            if oc is not None:
                name = company_map.get(int(oc))
                if name:
                    trow["fusion_company_name"] = name

        cust = fusion_data.get("customer") or {}
        tam_rows = fusion_data.get("tam") or []
        tam_parts = []
        for t in tam_rows[:2]:
            fn = (t.get("first_name") or "").strip()
            ln = (t.get("last_name") or "").strip()
            em = t.get("email_address") or ""
            label = f"{fn} {ln}".strip() or em
            if em and label != em:
                label = f"{label} <{em}>"
            elif not label:
                label = em
            if label:
                tam_parts.append(label)
        tam_display = "; ".join(tam_parts) if tam_parts else None

        view = TContextView(
            issue_key=issue_key,
            summary=ticket.get("summary") or "",
            status=ticket.get("status") or "",
            client_id=resolved_client,
            customer_name=cust.get("company_name"),
            tam_display=tam_display,
            fusion_error=fusion_data.get("fusion_error"),
            mssql_error=mssql_data.get("mssql_error"),
            customer_tickets=customer_tickets,
            components_sample=comps,
            neighbor_services=neigh_svcs,
            neighbor_tickets=neighbor_tickets,
            ticket_fusion_services=fusion_data.get("ticket_services_fusion") or [],
            fusion_services_for_client=fusion_data.get("services") or [],
        )

        return view.to_template_dict() | {"prompt_block": view.prompt_block()}
