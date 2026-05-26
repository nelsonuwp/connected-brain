#!/usr/bin/env python3
"""
pricebook_cost_gap.py

Full-coverage view of all is_available pricebook SKUs vs. profitability.ocean_sku_cost.
Gaps (SKUs missing from ocean_sku_cost) sort to the top. All pricebook currencies
pivot to their own columns: USD_MRC, USD_NRC, CAD_MRC, CAD_NRC, etc.

Uses credentials from cpq-front-end/.env and .env.local.

Usage:
    python pricebook_cost_gap.py [--output /path/to/report.csv]
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# Load credentials from cpq-front-end .env files
_project_dir = Path(__file__).resolve().parent.parent / "projects" / "cpq-front-end"
from dotenv import load_dotenv
load_dotenv(_project_dir / ".env")
load_dotenv(_project_dir / ".env.local", override=True)

import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from sshtunnel import SSHTunnelForwarder
import pymssql

# ── Fusion credentials ────────────────────────────────────────────────────────

SSH_HOST     = os.environ.get("SSH_HOST", "10.121.21.20")
SSH_PORT     = int(os.environ.get("SSH_PORT", "22"))
SSH_USER     = os.environ.get("SSH_USER", "")
SSH_PASSWORD = os.environ.get("SSH_PASS", "")

FUSION_HOST  = os.environ.get("FUSION_DB_SERVER", "db1.peer1.com")
FUSION_PORT  = int(os.environ.get("FUSION_DB_PORT", "5432"))
FUSION_DB    = os.environ.get("FUSION_DB_NAME", "fusion")
FUSION_USER  = os.environ.get("FUSION_DB_USER", "sb_readonly")
FUSION_PASS  = os.environ.get("FUSION_DB_PASS", "")

# ── MSSQL credentials ─────────────────────────────────────────────────────────

MSSQL_SERVER = os.environ.get("MSSQL_BI_SERVER", "")
MSSQL_DB     = os.environ.get("MSSQL_BI_NAME", "DM_BusinessInsights")
MSSQL_USER   = os.environ.get("MSSQL_BI_USER", "")
MSSQL_PASS   = os.environ.get("MSSQL_BI_PASS", "")


# ── Data fetching ─────────────────────────────────────────────────────────────

def fetch_pricebook() -> pd.DataFrame:
    """
    Returns all is_available pricebook rows with resolved SKU names.
    - Server rows (component_id IS NULL):  fusion_id = product_catalog_id, sku_level_pb = 'TLS'
    - Component rows (component_id IS NOT NULL): fusion_id = component_id, sku_level_pb = 'Component'
    """
    use_tunnel = bool(SSH_USER and SSH_PASSWORD)
    tunnel = None
    try:
        if use_tunnel:
            print(f"  → SSH tunnel via {SSH_HOST} ...", flush=True)
            tunnel = SSHTunnelForwarder(
                (SSH_HOST, SSH_PORT),
                ssh_username=SSH_USER,
                ssh_password=SSH_PASSWORD,
                remote_bind_address=(FUSION_HOST, FUSION_PORT),
            )
            tunnel.start()
            host, port = "127.0.0.1", tunnel.local_bind_port
        else:
            host, port = FUSION_HOST, FUSION_PORT

        conn = psycopg2.connect(
            host=host, port=port,
            dbname=FUSION_DB, user=FUSION_USER, password=FUSION_PASS,
            gssencmode="disable", cursor_factory=RealDictCursor,
        )
        conn.set_session(readonly=True, autocommit=True)

        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    CASE WHEN pb.component_id IS NOT NULL
                         THEN pb.component_id
                         ELSE pb.product_catalog_id END     AS fusion_id,
                    CASE WHEN pb.component_id IS NOT NULL
                         THEN 'Component'
                         ELSE 'TLS' END                     AS sku_level_pb,
                    COALESCE(c.display_name, pc.name, '')   AS sku_name_pb,
                    pb.is_available,
                    CASE WHEN pb.component_id IS NULL
                         THEN 'Server'
                         ELSE COALESCE(cc.name, '')
                    END                                     AS fusion_category,
                    CASE WHEN pb.component_id IS NULL
                         THEN ''
                         ELSE COALESCE(ct.name, '')
                    END                                     AS fusion_type,
                    pb.currency,
                    pb.datacenter,
                    COALESCE(pb.mrc, 0)::float              AS mrc,
                    COALESCE(pb.nrc, 0)::float              AS nrc
                FROM public.pricebook pb
                LEFT JOIN public.product_catalog pc
                       ON pc.id = pb.product_catalog_id
                      AND pb.component_id IS NULL
                LEFT JOIN public.components c
                       ON c.id = pb.component_id
                LEFT JOIN public.component_types ct
                       ON ct.id = c.component_type_id
                LEFT JOIN public.component_categories cc
                       ON cc.id = ct.category_id
                WHERE pb.is_available = true
                ORDER BY fusion_id, pb.currency
            """)
            rows = cur.fetchall()
        conn.close()
        print(f"  → {len(rows)} pricebook rows fetched", flush=True)
        return pd.DataFrame([dict(r) for r in rows])
    finally:
        if tunnel:
            tunnel.stop()


def fetch_ocean_sku_cost() -> pd.DataFrame:
    """Returns all rows from profitability.ocean_sku_cost."""
    conn = pymssql.connect(
        server=MSSQL_SERVER, user=MSSQL_USER,
        password=MSSQL_PASS, database=MSSQL_DB,
        tds_version="7.0",
    )
    cur = conn.cursor(as_dict=True)
    cur.execute("""
        SELECT
            sku_id,
            sku_name,
            sku_level,
            sku_category,
            sku_type,
            CAST(sku_cost AS FLOAT) AS sku_cost,
            cost_currency,
            vendor
        FROM profitability.ocean_sku_cost
    """)
    rows = [dict(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    print(f"  → {len(rows)} ocean_sku_cost rows fetched", flush=True)
    return pd.DataFrame(rows)


def fetch_active_component_counts() -> pd.DataFrame:
    """
    Returns a count of online deployments per component_id from dimComponents,
    filtered to active services only.
    Columns: fusion_id, active_deployments
    """
    conn = pymssql.connect(
        server=MSSQL_SERVER, user=MSSQL_USER,
        password=MSSQL_PASS, database=MSSQL_DB,
        tds_version="7.0",
    )
    cur = conn.cursor(as_dict=True)
    cur.execute("""
        SELECT dc.component_id, COUNT(*) AS active_deployments
        FROM DM_BusinessInsights.dbo.dimComponents dc
        JOIN DM_BusinessInsights.dbo.dimServices ds
          ON ds.service_id = dc.service_id
        WHERE dc.is_online = 'Yes'
          AND ds.service_status = 'Online'
        GROUP BY dc.component_id
    """)
    rows = [dict(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    print(f"  → {len(rows)} component deployment counts fetched", flush=True)
    df = pd.DataFrame(rows) if rows else pd.DataFrame(columns=["component_id", "active_deployments"])
    return df.rename(columns={"component_id": "fusion_id"})


# ── Report building ───────────────────────────────────────────────────────────

def pivot_pricebook(pb: pd.DataFrame) -> pd.DataFrame:
    """
    Collapses pricebook to one row per (fusion_id, sku_level_pb, sku_name_pb).
    Where the same fusion_id appears in multiple datacenters for the same currency,
    takes the minimum (most conservative) MRC/NRC.
    Currencies become columns: USD_MRC, USD_NRC, CAD_MRC, CAD_NRC, etc.
    USD appears first, then CAD, then all others alphabetically.
    """
    # One value per (fusion_id, currency) — min across datacenters
    agg = pb.groupby(
        ["fusion_id", "sku_level_pb", "sku_name_pb", "is_available", "fusion_category", "fusion_type", "currency"],
        as_index=False,
    ).agg(mrc=("mrc", "min"), nrc=("nrc", "min"))

    mrc_pivot = agg.pivot_table(
        index=["fusion_id", "sku_level_pb", "sku_name_pb", "is_available", "fusion_category", "fusion_type"],
        columns="currency",
        values="mrc",
        aggfunc="first",
    )
    mrc_pivot.columns = [f"{c}_MRC" for c in mrc_pivot.columns]

    nrc_pivot = agg.pivot_table(
        index=["fusion_id", "sku_level_pb", "sku_name_pb", "is_available", "fusion_category", "fusion_type"],
        columns="currency",
        values="nrc",
        aggfunc="first",
    )
    nrc_pivot.columns = [f"{c}_NRC" for c in nrc_pivot.columns]

    wide = mrc_pivot.join(nrc_pivot).reset_index()

    # Order currency columns: USD first, CAD second, rest alphabetically
    price_cols = [c for c in wide.columns if c.endswith("_MRC") or c.endswith("_NRC")]
    currencies = sorted(
        set(c.rsplit("_", 1)[0] for c in price_cols),
        key=lambda x: (x != "USD", x != "CAD", x),
    )
    ordered = [f"{cur}_{sfx}" for cur in currencies for sfx in ("MRC", "NRC")]
    ordered = [c for c in ordered if c in wide.columns]

    id_cols = [c for c in wide.columns if c not in ordered]
    return wide[id_cols + ordered]


def build_report(output_path: str):
    print("\n[1/2] Fetching Fusion pricebook...")
    pb = fetch_pricebook()
    if pb.empty:
        print("ERROR: No pricebook rows returned. Check Fusion credentials/SSH config.")
        sys.exit(1)

    print("\n[2/3] Fetching MSSQL ocean_sku_cost...")
    costs = fetch_ocean_sku_cost()

    print("\n[3/3] Fetching active deployment counts from dimComponents...")
    deploy_counts = fetch_active_component_counts()

    print("\nBuilding report...")

    # Pivot pricebook to one row per fusion_id with currency columns
    pb_wide = pivot_pricebook(pb)
    pb_wide["fusion_id"] = pb_wide["fusion_id"].astype(int)

    # Prep ocean_sku_cost for joining
    costs["sku_id"] = costs["sku_id"].astype(int)
    costs_j = costs.rename(columns={"sku_id": "fusion_id", "sku_level": "sku_level_osc"})

    # Left-join on (fusion_id, sku_level) so server rows only match TLS costs
    # and component rows only match Component costs — avoids ID-space collisions.
    merged = pb_wide.merge(
        costs_j,
        left_on=["fusion_id", "sku_level_pb"],
        right_on=["fusion_id", "sku_level_osc"],
        how="left",
    )

    merged["has_cost"] = merged["sku_cost"].notna()

    # Join active deployment counts (component rows only; TLS rows won't match, get 0)
    deploy_counts["fusion_id"] = deploy_counts["fusion_id"].astype(int)
    merged = merged.merge(deploy_counts, on="fusion_id", how="left")
    merged["active_deployments"] = merged["active_deployments"].fillna(0).astype(int)

    # Final column order
    id_cols    = ["fusion_id", "sku_name_pb", "sku_level_pb", "is_available",
                  "fusion_category", "fusion_type", "active_deployments"]
    cost_cols  = ["sku_name", "sku_level_osc", "sku_category", "sku_type",
                  "sku_cost", "cost_currency", "vendor"]
    price_cols = [c for c in merged.columns if c.endswith("_MRC") or c.endswith("_NRC")]
    flag_cols  = ["has_cost"]

    all_cols = flag_cols + id_cols + cost_cols + price_cols
    all_cols = [c for c in all_cols if c in merged.columns]

    result = (
        merged[all_cols]
        .sort_values(["has_cost", "sku_name_pb"], ascending=[True, True])
        .reset_index(drop=True)
    )

    result.to_csv(output_path, index=False)

    gap_count = int((~result["has_cost"]).sum())
    covered   = int(result["has_cost"].sum())
    print(f"\n✅  {output_path}")
    print(f"   Total rows : {len(result)}")
    print(f"   Gaps       : {gap_count}  (no entry in ocean_sku_cost)")
    print(f"   Have cost  : {covered}")


def main():
    parser = argparse.ArgumentParser(
        description="Pricebook vs. ocean_sku_cost gap report"
    )
    parser.add_argument(
        "--output", "-o",
        default=str(
            Path(__file__).parent /
            f"pricebook_cost_gap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        ),
        help="Output CSV path (default: same dir as script, timestamped)",
    )
    args = parser.parse_args()
    build_report(args.output)


if __name__ == "__main__":
    main()
