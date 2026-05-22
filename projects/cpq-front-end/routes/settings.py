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


@settings_bp.route("/api/settings/overhead", methods=["POST"])
def settings_overhead_post():
    data = request.get_json(force=True)

    try:
        sga = float(data.get("overhead_constants", {}).get("sga_pct", -1))
        if not (0 <= sga <= 1):
            return jsonify({"error": "sga_pct must be between 0 and 1"}), 400
    except (TypeError, ValueError):
        return jsonify({"error": "sga_pct must be a number"}), 400

    service_types = ["server", "firewall", "switch"]
    for dc_abbr, dc in data.get("data_centers", {}).items():
        for svc in service_types:
            for key, entry in dc.get("costs", {}).get(svc, {}).items():
                try:
                    if float(entry.get("amount", -1)) < 0:
                        return jsonify({"error": f"{dc_abbr}.{svc}.{key}: amount must be >= 0"}), 400
                except (TypeError, ValueError):
                    return jsonify({"error": f"{dc_abbr}.{svc}.{key}: amount must be a number"}), 400

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
