#!/usr/bin/env python3
"""
Diagnostic: find a server renewal service and validate what the API would compute.
Run from project root: python scripts/investigate_renewal.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(".env")
load_dotenv(".env.local", override=True)

import pymssql
from db.mssql import _connect as mssql_connect, _configured as mssql_ok, get_renewal_services
from db.fusion import get_conn as fusion_conn, get_dc_info, get_dc_registry

SEP = "-" * 70

def mssql_cur():
    conn = mssql_connect()
    return conn, conn.cursor(as_dict=True)

def fusion_cur():
    conn = fusion_conn()
    return conn, conn.cursor()

# ── 1. Find a few server renewal services ────────────────────────────────────
print(SEP)
print("STEP 1 — Find server renewal services (non-m2m, real exp date)")
print(SEP)
conn_ms, cur_ms = mssql_cur()
cur_ms.execute("""
    SELECT TOP 5
        osrd.service_id, osrd.client_id, osrd.company_name,
        osrd.expiration_date, osrd.m2m,
        ds.product, ds.datacenter_code, ds.currency, ds.mrc,
        ds.fusion_id, ds.service_type
    FROM DM_BusinessInsights.renewals.ocean_services_renewal_date osrd
    JOIN DM_BusinessInsights.dbo.dimServices ds ON ds.service_id = osrd.service_id
    WHERE osrd.m2m != 'yes'
      AND osrd.expiration_date > '1900-01-01'
      AND ds.service_type LIKE '%Server%'
    ORDER BY osrd.expiration_date ASC
""")
services = cur_ms.fetchall()
for s in services:
    print(f"  svc={s['service_id']}  client={s['client_id']}  co={s['company_name']}")
    print(f"       exp={s['expiration_date']}  m2m={s['m2m']}  type={s['service_type']}")
    print(f"       dc={s['datacenter_code']}  fusion_id={s['fusion_id']}  cur={s['currency']}  mrc={s['mrc']}")
    print()

if not services:
    print("  (no server renewals found — trying any type)")
    cur_ms.execute("""
        SELECT TOP 5
            osrd.service_id, osrd.client_id, osrd.company_name,
            osrd.expiration_date, osrd.m2m,
            ds.product, ds.datacenter_code, ds.currency, ds.mrc,
            ds.fusion_id, ds.service_type
        FROM DM_BusinessInsights.renewals.ocean_services_renewal_date osrd
        JOIN DM_BusinessInsights.dbo.dimServices ds ON ds.service_id = osrd.service_id
        WHERE osrd.m2m != 'yes'
          AND osrd.expiration_date > '1900-01-01'
        ORDER BY osrd.expiration_date ASC
    """)
    services = cur_ms.fetchall()
    for s in services:
        print(f"  svc={s['service_id']}  dc={s['datacenter_code']}  fusion_id={s['fusion_id']}")

if not services:
    print("ERROR: no renewal services found at all")
    sys.exit(1)

TARGET = services[0]
SVC_ID     = TARGET["service_id"]
DC_CODE    = (TARGET["datacenter_code"] or "").upper()
FUSION_PID = TARGET["fusion_id"]

print(f"\nUsing service_id={SVC_ID}, dc_code={DC_CODE!r}, fusion_pid={FUSION_PID}")

# ── 2. Check DC registry in Fusion ───────────────────────────────────────────
print(SEP)
print(f"STEP 2 — DC registry lookup for '{DC_CODE}'")
print(SEP)
registry = get_dc_registry()
print(f"  DCs in registry: {sorted(registry.keys())}")
dc_info = get_dc_info(DC_CODE)
if dc_info:
    print(f"  FOUND: id={dc_info['id']}  native_currency={dc_info['native_currency']}")
    FUSION_DC_ID = dc_info["id"]
else:
    print(f"  NOT FOUND for '{DC_CODE}' — this is why dc_not_in_fusion fires!")
    FUSION_DC_ID = None

# ── 3. Inspect dimComponents for this service ────────────────────────────────
print(SEP)
print(f"STEP 3 — dimComponents for service_id={SVC_ID}")
print(SEP)
cur_ms.execute("""
    SELECT component_category, component_type, component, component_id,
           component_mrc, product_mrc, currency, is_online
    FROM DM_BusinessInsights.dbo.dimComponents
    WHERE service_id = %d
    ORDER BY component_category, component_type, component
""", (SVC_ID,))
comps = cur_ms.fetchall()
for c in comps:
    print(f"  [{c['component_category']}] {c['component']}")
    print(f"       id={c['component_id']}  mrc={c['component_mrc']}  online={c['is_online']}")

# ── 4. Check pricebook for a few component_ids ───────────────────────────────
print(SEP)
print("STEP 4 — Fusion pricebook check for first few component IDs")
print(SEP)
conn_f, cur_f = fusion_cur()
cids = [c["component_id"] for c in comps if c["component_id"]][:8]
print(f"  Checking component_ids: {cids}")
for cid in cids:
    cur_f.execute("""
        SELECT component_id, currency, datacenter, mrc, is_available
        FROM public.pricebook
        WHERE component_id = %s
        ORDER BY datacenter, currency
        LIMIT 10
    """, (cid,))
    rows = cur_f.fetchall()
    if rows:
        print(f"  cid={cid}: {len(rows)} pricebook rows")
        for r in rows[:4]:
            print(f"    dc={r['datacenter']} cur={r['currency']} mrc={r['mrc']} avail={r['is_available']}")
    else:
        print(f"  cid={cid}: NO pricebook rows at all")

# ── 5. Check product_allowed_components ──────────────────────────────────────
if FUSION_PID:
    print(SEP)
    print(f"STEP 5 — product_allowed_components for fusion_pid={FUSION_PID}")
    print(SEP)
    cur_f.execute("""
        SELECT pac.component_id, c.name, c.is_active
        FROM public.product_allowed_components pac
        LEFT JOIN public.components c ON c.id = pac.component_id
        WHERE pac.product_id = %s
        ORDER BY pac.component_id
    """, (FUSION_PID,))
    allowed = cur_f.fetchall()
    if allowed:
        print(f"  {len(allowed)} allowed components for product {FUSION_PID}:")
        for a in allowed:
            print(f"    cid={a['component_id']}  name={a['name']}  active={a['is_active']}")
    else:
        print(f"  NO entries in product_allowed_components for product {FUSION_PID}")
        # Check if the product exists at all
        cur_f.execute("SELECT id, name FROM public.product_catalog WHERE id = %s", (FUSION_PID,))
        pc = cur_f.fetchone()
        if pc:
            print(f"  Product exists: {dict(pc)}")
        else:
            print(f"  Product {FUSION_PID} does NOT exist in public.product_catalog!")

# ── 6. Specific check on component 3538 ──────────────────────────────────────
print(SEP)
print("STEP 6 — Component ID 3538 details")
print(SEP)
cur_f.execute("SELECT id, name, is_active FROM public.components WHERE id = 3538")
comp_row = cur_f.fetchone()
if comp_row:
    print(f"  components row: {dict(comp_row)}")
else:
    print("  id=3538 not in public.components")

cur_f.execute("""
    SELECT component_id, currency, datacenter, mrc, is_available
    FROM public.pricebook
    WHERE component_id = 3538
    ORDER BY datacenter, currency
""")
pb_rows = cur_f.fetchall()
if pb_rows:
    print(f"  pricebook rows for 3538: {len(pb_rows)}")
    for r in pb_rows:
        print(f"    dc={r['datacenter']} cur={r['currency']} mrc={r['mrc']} avail={r['is_available']}")
else:
    print("  NO pricebook rows for 3538")

# ── 7. Check what dc IDs the pricebook uses if DC was found ──────────────────
if FUSION_DC_ID and cids:
    print(SEP)
    print(f"STEP 7 — Pricebook for dc={FUSION_DC_ID} for our component IDs")
    print(SEP)
    for cid in cids[:4]:
        cur_f.execute("""
            SELECT component_id, currency, datacenter, mrc, is_available
            FROM public.pricebook
            WHERE component_id = %s AND datacenter = %s
            LIMIT 5
        """, (cid, FUSION_DC_ID))
        rows = cur_f.fetchall()
        if rows:
            print(f"  cid={cid} + dc={FUSION_DC_ID}: {len(rows)} rows")
            for r in rows:
                print(f"    cur={r['currency']} mrc={r['mrc']} avail={r['is_available']}")
        else:
            print(f"  cid={cid} + dc={FUSION_DC_ID}: no rows (trying without dc filter)")
            cur_f.execute("""
                SELECT datacenter, currency, mrc, is_available
                FROM public.pricebook WHERE component_id = %s LIMIT 5
            """, (cid,))
            rows2 = cur_f.fetchall()
            if rows2:
                for r in rows2:
                    print(f"    dc={r['datacenter']} cur={r['currency']} mrc={r['mrc']} avail={r['is_available']}")

# ── 8. Summary ────────────────────────────────────────────────────────────────
print(SEP)
print("SUMMARY")
print(SEP)
print(f"  service_id:    {SVC_ID}")
print(f"  dc_code:       {DC_CODE!r}")
print(f"  fusion_pid:    {FUSION_PID}")
print(f"  fusion_dc_id:  {FUSION_DC_ID}")
print(f"  dc registry:   {sorted(registry.keys())}")
if not FUSION_DC_ID:
    print("\n  ROOT CAUSE: DC code not found in registry → all comps get dc_not_in_fusion")
if FUSION_PID is None:
    print("\n  ROOT CAUSE: fusion_id is NULL on service → pricebook lookup skipped entirely")
