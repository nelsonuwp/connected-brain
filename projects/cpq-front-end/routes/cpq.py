from flask import Blueprint, jsonify, render_template, request

from db.fusion import dec, get_conn, get_dc_info, get_dc_registry
from db.mssql import get_fx_rate, get_mssql_costs, get_mssql_watts
from lib.overhead import calc_overhead

cpq_bp = Blueprint("cpq", __name__)


@cpq_bp.route("/")
def index():
    return render_template("index.html", active_page="quotes")


@cpq_bp.route("/product/<int:product_id>")
def product_page(product_id):
    return render_template("product.html", product_id=product_id, active_page="quotes")


@cpq_bp.route("/api/datacenters")
def datacenters():
    registry = get_dc_registry()
    return jsonify([
        {
            "code": info["dc_abbr"], "name": info["name"],
            "fusion_dc_id": info["id"], "currencies": info["currencies"],
            "native_currency": info["native_currency"],
        }
        for info in sorted(registry.values(), key=lambda x: x["dc_abbr"])
    ])


@cpq_bp.route("/api/fx-rate")
def fx_rate_endpoint():
    from_cur = request.args.get("from", "USD").upper()
    to_cur   = request.args.get("to",   "USD").upper()
    rate     = get_fx_rate(from_cur, to_cur)
    return jsonify({"from": from_cur, "to": to_cur, "rate": rate})


@cpq_bp.route("/api/servers")
def servers():
    dc_abbr      = request.args.get("dc", "").upper()
    currency     = request.args.get("currency", "USD").upper()
    product_line = request.args.get("product_line", "4")

    dc_info = get_dc_info(dc_abbr)
    if not dc_info:
        return jsonify({"error": f"Unknown DC: {dc_abbr}"}), 400

    fusion_dc_id    = dc_info["id"]
    native_currency = dc_info["native_currency"]

    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT pc.id, pc.name, pc.description, pc.sku,
                   pc.available_in_shop, pc.sold_out, pc.limited_availability,
                   pb_disp.id   AS pb_disp_id,
                   pb_disp.mrc  AS disp_mrc,  pb_disp.nrc  AS disp_nrc,
                   pb_disp.setup AS disp_setup, pb_disp.is_available AS disp_available,
                   pb_nat.id    AS pb_nat_id,
                   pb_nat.mrc   AS nat_mrc,   pb_nat.nrc   AS nat_nrc,
                   pb_nat.setup  AS nat_setup,  pb_nat.is_available  AS nat_available
            FROM public.product_catalog pc
            LEFT JOIN LATERAL (
                SELECT id, mrc, nrc, setup, is_available
                FROM public.pricebook
                WHERE product_catalog_id = pc.id AND currency = %s
                  AND datacenter = %s AND product_line_id = %s AND component_id IS NULL
                LIMIT 1
            ) pb_disp ON true
            LEFT JOIN LATERAL (
                SELECT id, mrc, nrc, setup, is_available
                FROM public.pricebook
                WHERE product_catalog_id = pc.id AND currency = %s
                  AND datacenter = %s AND product_line_id = %s AND component_id IS NULL
                LIMIT 1
            ) pb_nat ON true
            WHERE pc.product_class = 1 AND pc.is_active = true
              AND EXISTS (
                  SELECT 1 FROM public.pricebook
                  WHERE product_catalog_id = pc.id AND datacenter = %s
                    AND product_line_id = %s AND component_id IS NULL
              )
            ORDER BY COALESCE(pb_disp.mrc, pb_nat.mrc) ASC NULLS LAST
        """, (
            currency, fusion_dc_id, product_line,
            native_currency, fusion_dc_id, product_line,
            fusion_dc_id, product_line,
        ))
        rows = cur.fetchall()

    fx_native_to_display = (
        get_fx_rate(native_currency, currency) if native_currency != currency else 1.0
    )

    result = []
    for r in rows:
        warnings = []
        if r["pb_disp_id"] is not None:
            mrc_pb = dec(r["disp_mrc"]); nrc_pb = dec(r["disp_nrc"])
            setup_pb = dec(r["disp_setup"]); fx = 1.0
            pb_id = r["pb_disp_id"]; is_avail = r["disp_available"]
            pricing_cur = currency
        elif r["pb_nat_id"] is not None:
            mrc_pb = dec(r["nat_mrc"]); nrc_pb = dec(r["nat_nrc"])
            setup_pb = dec(r["nat_setup"]); fx = fx_native_to_display
            pb_id = r["pb_nat_id"]; is_avail = r["nat_available"]
            pricing_cur = native_currency
            if native_currency != currency:
                warnings.append("no_pricebook_in_display_currency")
        else:
            mrc_pb = nrc_pb = setup_pb = fx = 0.0
            pb_id = is_avail = pricing_cur = None
            warnings.append("no_pricebook_row")

        if pb_id is not None and mrc_pb == 0:
            warnings.append("mrc_is_zero")
        if is_avail is False:
            warnings.append("not_available_in_pricebook")

        result.append({
            "id": r["id"], "name": r["name"], "description": r["description"],
            "sku": r["sku"], "available_in_shop": r["available_in_shop"],
            "sold_out": r["sold_out"], "limited_availability": r["limited_availability"],
            "pricebook_id": pb_id,
            "mrc": round(mrc_pb * fx, 2) if pb_id is not None else None,
            "nrc": round(nrc_pb * fx, 2), "setup": round(setup_pb * fx, 2),
            "is_available": is_avail, "pricing_currency": pricing_cur,
            "display_currency": currency, "fx_pricing": fx, "warnings": warnings,
        })

    return jsonify(result)


@cpq_bp.route("/api/product/<int:product_id>")
def product_detail(product_id):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, name, description, sku, is_active,
                   available_in_shop, sold_out, limited_availability, release_date
            FROM public.product_catalog WHERE id = %s
        """, (product_id,))
        row = cur.fetchone()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(dict(row))


@cpq_bp.route("/api/product/<int:product_id>/config")
def product_config(product_id):
    dc_abbr      = request.args.get("dc", "ATL").upper()
    currency     = request.args.get("currency", "USD").upper()
    product_line = request.args.get("product_line", "4")
    term_months  = int(request.args.get("term", "36"))

    dc_info = get_dc_info(dc_abbr)
    if not dc_info:
        return jsonify({"error": f"Unknown DC: {dc_abbr}"}), 400

    fusion_dc_id    = dc_info["id"]
    native_currency = dc_info["native_currency"]
    fx_overhead     = get_fx_rate(native_currency, currency)

    conn = get_conn()

    def _query_server_pb(pb_currency):
        with conn.cursor() as cur:
            cur.execute("""
                SELECT pb.id AS pricebook_id, pb.mrc, pb.nrc, pb.setup
                FROM public.pricebook pb
                WHERE pb.product_catalog_id = %s AND pb.component_id IS NULL
                  AND pb.currency = %s AND pb.datacenter = %s
                  AND pb.product_line_id = %s AND pb.is_available = true
                LIMIT 1
            """, (product_id, pb_currency, fusion_dc_id, product_line))
            return cur.fetchone()

    pb_row = _query_server_pb(currency)
    if pb_row:
        pricing_currency = currency; fx_pricing = 1.0
    else:
        pb_row = _query_server_pb(native_currency)
        pricing_currency = native_currency
        fx_pricing = get_fx_rate(native_currency, currency)

    server_mrc_pb   = dec(pb_row["mrc"])   if pb_row else 0
    server_nrc_pb   = dec(pb_row["nrc"])   if pb_row else 0
    server_setup_pb = dec(pb_row["setup"]) if pb_row else 0
    server_mrc      = round(server_mrc_pb   * fx_pricing, 2)
    server_nrc      = round(server_nrc_pb   * fx_pricing, 2)
    server_setup    = round(server_setup_pb * fx_pricing, 2)
    pricebook_id    = pb_row["pricebook_id"] if pb_row else None

    pb_provenance = {
        "source": "Fusion: public.pricebook",
        "filters": (
            f"product_catalog_id={product_id}, currency={pricing_currency}, "
            f"datacenter={fusion_dc_id} ({dc_abbr}), product_line_id={product_line}, "
            f"component_id IS NULL, is_available=true"
        ),
        "pricebook_id": pricebook_id, "field": "pricebook.mrc",
        "pb_value": server_mrc_pb, "pricing_currency": pricing_currency,
        "fx_pricing": fx_pricing,
        "fx_source": (
            f"MSSQL: dbo.dimCurrencyExchangeRates "
            f"WHERE from_currency='{pricing_currency}' AND to_currency='{currency}'"
        ) if fx_pricing != 1.0 else "direct — no conversion needed",
        "display_value": server_mrc, "display_currency": currency,
    }

    def _query_components(table, id_col, pb_currency):
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT t.{id_col} AS component_id,
                       {'t.quantity,' if table == 'public.product_templates' else '1 AS quantity,'}
                       c.display_name AS name, c.description, c.is_active,
                       ct.name AS component_type, pct.name AS parent_type,
                       cc.name AS category, cc.sort_order AS cat_sort,
                       pb.id AS pricebook_id,
                       pb.mrc AS component_mrc, pb.nrc AS component_nrc,
                       pb.setup AS component_setup, pb.product_line_id AS pb_product_line_id
                FROM {table} t
                JOIN public.components c ON c.id = t.{id_col}
                JOIN public.component_types ct ON ct.id = c.component_type_id
                LEFT JOIN public.component_types pct ON pct.id = ct.parent_component_id
                JOIN public.component_categories cc ON cc.id = ct.category_id
                LEFT JOIN LATERAL (
                    SELECT id, mrc, nrc, setup, product_line_id FROM public.pricebook
                    WHERE component_id = t.{id_col} AND currency = %s
                      AND datacenter = %s AND is_available = true
                    ORDER BY (product_line_id = %s) DESC, product_line_id
                    LIMIT 1
                ) pb ON true
                WHERE t.product_id = %s
                {'AND c.is_active = true' if table == 'public.product_allowed_components' else ''}
                ORDER BY cc.sort_order, cc.name, ct.name, c.display_name
            """, (pb_currency, fusion_dc_id, product_line, product_id))
            return cur.fetchall()

    defaults_raw = _query_components("public.product_templates", "component_id", pricing_currency)
    allowed_raw  = _query_components("public.product_allowed_components", "component_id", pricing_currency)

    component_ids = list(
        {r["component_id"] for r in defaults_raw} | {r["component_id"] for r in allowed_raw}
    )
    hw_costs_comp = get_mssql_costs(component_ids, "Component") if component_ids else {}
    hw_costs_tls  = get_mssql_costs([product_id], "TLS")
    hw_costs      = {**hw_costs_comp, **hw_costs_tls}

    cost_currencies = {v["currency"] for v in hw_costs.values() if v.get("currency")}
    fx_cost_map     = {c: get_fx_rate(c, currency) for c in cost_currencies}

    def _fmt_component(r, is_default=False, quantity=1):
        cid = r["component_id"]
        mrc_pb = dec(r["component_mrc"])
        nrc_pb = dec(r["component_nrc"])
        addon_mrc_display   = round(mrc_pb * fx_pricing, 2)
        addon_nrc_display   = round(nrc_pb * fx_pricing, 2)
        setup_pb            = dec(r.get("component_setup") or 0)
        addon_setup_display = round(setup_pb * fx_pricing, 2)
        mrc_display   = 0.0 if is_default else addon_mrc_display
        nrc_display   = 0.0 if is_default else addon_nrc_display
        setup_display = 0.0 if is_default else addon_setup_display
        pb_id = r.get("pricebook_id")

        hw = hw_costs.get(cid)
        if hw:
            hw_cost_raw = hw["cost"]; hw_cost_currency = hw["currency"]
            fx_cost = fx_cost_map.get(hw_cost_currency, 1.0)
            hw_cost_display = round(hw_cost_raw * fx_cost, 2)
            cost_kind = hw.get("cost_kind", "hw")
        else:
            hw_cost_raw = hw_cost_currency = fx_cost = hw_cost_display = cost_kind = None

        return {
            "component_id": cid, "name": r["name"],
            "description": r["description"] or "", "is_active": r["is_active"],
            "component_type": r["component_type"], "parent_type": r.get("parent_type"),
            "category": r["category"], "cat_sort": r["cat_sort"], "quantity": quantity,
            "component_mrc": mrc_display, "component_nrc": nrc_display,
            "component_setup": setup_display, "addon_mrc": addon_mrc_display,
            "addon_setup": addon_setup_display, "hw_cost_raw": hw_cost_raw,
            "hw_cost_currency": hw_cost_currency, "hw_cost_display": hw_cost_display,
            "cost_kind": cost_kind, "is_default": is_default,
            "pricebook_provenance": {
                "source": "Fusion: public.pricebook", "pricebook_id": pb_id,
                "field": "pricebook.mrc",
                "filters": (
                    f"component_id={cid}, currency={pricing_currency}, "
                    f"datacenter={fusion_dc_id} ({dc_abbr}), "
                    f"product_line_id={product_line}, is_available=true"
                ),
                "pb_value": mrc_pb, "pricing_currency": pricing_currency,
                "fx_pricing": fx_pricing, "display_value": addon_mrc_display,
                "display_currency": currency, "included_in_base": is_default,
            } if pb_id else None,
            "hw_provenance": {
                "source": "MSSQL: DM_BusinessInsights.profitability.ocean_sku_cost",
                "field": "sku_cost", "sku_id": cid,
                "sku_name": hw["name"] if hw else None,
                "cost_value": hw_cost_raw, "cost_currency": hw_cost_currency,
                "fx_cost": fx_cost,
                "fx_source": (
                    f"dbo.dimCurrencyExchangeRates WHERE from_currency='{hw_cost_currency}' "
                    f"AND to_currency='{currency}' ORDER BY start_date DESC"
                ) if hw_cost_currency and hw_cost_currency != currency else None,
                "display_value": hw_cost_display, "display_currency": currency,
                "formula": (
                    f"{hw_cost_raw} {hw_cost_currency} × {fx_cost} = {hw_cost_display} {currency}"
                    if hw_cost_raw else "Not in ocean_sku_cost"
                ),
            } if hw else None,
        }

    defaults    = [_fmt_component(r, is_default=True, quantity=r["quantity"]) for r in defaults_raw]
    allowed     = [_fmt_component(r, is_default=False) for r in allowed_raw]
    default_ids = {r["component_id"] for r in defaults_raw}

    total_mrc = server_mrc + sum(
        d["component_mrc"] * d["quantity"] for d in defaults if d["component_mrc"] > 0
    )

    server_hw = hw_costs.get(product_id)
    if server_hw and server_hw["cost"] > 0:
        hw_capex_raw = server_hw["cost"]; hw_capex_currency = server_hw["currency"]
        fx_cost_server = fx_cost_map.get(hw_capex_currency, 1.0)
        total_hw_capex = round(hw_capex_raw * fx_cost_server, 2)
        hw_capex_method = "server-level"; hw_capex_sku_name = server_hw["name"]
    else:
        hw_capex_raw = sum(
            hw_costs[d["component_id"]]["cost"] * d["quantity"]
            if d["component_id"] in hw_costs else 0
            for d in defaults
        )
        first_hw = next((hw_costs[d["component_id"]] for d in defaults if d["component_id"] in hw_costs), None)
        hw_capex_currency = first_hw["currency"] if first_hw else "USD"
        fx_cost_server = fx_cost_map.get(hw_capex_currency, 1.0)
        total_hw_capex = round(hw_capex_raw * fx_cost_server, 2)
        hw_capex_method = "component-sum"; hw_capex_sku_name = None

    server_watts = get_mssql_watts(product_id)
    server_kw    = round(server_watts / 1000, 4) if server_watts is not None else None
    overhead     = calc_overhead(dc_abbr, total_mrc, fx_rate=fx_overhead, kw=server_kw)

    return jsonify({
        "product_id": product_id, "server_mrc": server_mrc,
        "server_nrc": server_nrc, "server_setup": server_setup,
        "currency": currency, "native_currency": native_currency,
        "pricing_currency": pricing_currency, "dc_code": dc_abbr,
        "fusion_dc_id": fusion_dc_id, "product_line": int(product_line),
        "term_months": term_months, "fx_pricing": fx_pricing,
        "fx_overhead": fx_overhead,
        "fx_source": "MSSQL: DM_BusinessInsights.dbo.dimCurrencyExchangeRates",
        "defaults": defaults, "allowed": allowed,
        "default_ids": list(default_ids),
        "server_watts": server_watts, "server_kw": server_kw,
        "overhead": overhead, "total_hw_capex": total_hw_capex,
        "hw_capex_cost": hw_capex_raw, "hw_capex_currency": hw_capex_currency,
        "hw_capex_provenance": {
            "source": "MSSQL: DM_BusinessInsights.profitability.ocean_sku_cost",
            "field": "sku_cost",
            "sku_id": product_id if hw_capex_method == "server-level" else "multiple",
            "sku_name": hw_capex_sku_name, "method": hw_capex_method,
            "cost_value": hw_capex_raw, "cost_currency": hw_capex_currency,
            "fx_cost": fx_cost_server,
            "fx_source": (
                f"dbo.dimCurrencyExchangeRates WHERE from_currency='{hw_capex_currency}' "
                f"AND to_currency='{currency}' ORDER BY start_date DESC"
            ) if hw_capex_currency != currency else "same currency — no conversion",
            "display_value": total_hw_capex, "display_currency": currency,
            "formula": f"{hw_capex_raw} {hw_capex_currency} × {fx_cost_server} = {total_hw_capex} {currency}",
        },
        "total_mrc": round(total_mrc, 2),
        "server_mrc_provenance": pb_provenance,
    })
