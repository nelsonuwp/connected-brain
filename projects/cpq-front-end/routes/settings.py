import json
import os

from flask import Blueprint, jsonify, render_template, request

from lib.overhead import COST_DRIVERS, reload as reload_cost_drivers

settings_bp = Blueprint("settings", __name__)


def _get_path():
    from pathlib import Path
    return Path(__file__).parent.parent / "cost_drivers.json"


@settings_bp.route("/settings")
def settings_page():
    return render_template("settings.html", active_page="settings")


@settings_bp.route("/api/settings/overhead", methods=["GET"])
def settings_overhead_get():
    return jsonify(COST_DRIVERS)


@settings_bp.route("/api/settings/service-types")
def settings_service_types():
    """All service types: from cost_drivers.json + distinct values in dimServices."""
    from db.mssql import _configured as mssql_configured
    json_types = set()
    for dc in COST_DRIVERS.get("data_centers", {}).values():
        for svc_type in dc.get("costs", {}).keys():
            json_types.add(svc_type)

    db_types = set()
    if mssql_configured():
        try:
            from db.profitability import get_profitability_filter_options
            opts = get_profitability_filter_options()
            db_types = set(opts.get("service_types", []))
        except Exception:
            pass

    all_types = sorted(json_types | db_types)
    return jsonify(all_types)


@settings_bp.route("/api/settings/overhead", methods=["POST"])
def settings_overhead_post():
    data = request.get_json(force=True)

    try:
        sga = float(data.get("overhead_constants", {}).get("sga_pct", -1))
        if not (0 <= sga <= 1):
            return jsonify({"error": "sga_pct must be between 0 and 1"}), 400
    except (TypeError, ValueError):
        return jsonify({"error": "sga_pct must be a number"}), 400

    for dc_abbr, dc in data.get("data_centers", {}).items():
        for svc_type, svc_costs in dc.get("costs", {}).items():
            for key, entry in svc_costs.items():
                amt = entry.get("amount")
                if amt is None:
                    continue  # null = no data configured, allowed
                try:
                    if float(amt) < 0:
                        return jsonify({"error": f"{dc_abbr}.{svc_type}.{key}: amount must be >= 0"}), 400
                except (TypeError, ValueError):
                    return jsonify({"error": f"{dc_abbr}.{svc_type}.{key}: amount must be a number"}), 400

    path = _get_path()
    tmp = path.with_suffix(".json.tmp")
    try:
        with open(tmp, "w") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        os.replace(tmp, path)
    except Exception as e:
        return jsonify({"error": f"Write failed: {e}"}), 500

    reload_cost_drivers()
    return jsonify({"ok": True})
