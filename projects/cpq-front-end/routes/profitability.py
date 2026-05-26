from flask import Blueprint, jsonify, render_template, request

profitability_bp = Blueprint("profitability", __name__)


@profitability_bp.route("/profitability")
def profitability_page():
    return render_template("profitability.html", active_page="profitability")


@profitability_bp.route("/profitability/<int:client_id>")
def profitability_customer_page(client_id):
    return render_template(
        "profitability_customer.html",
        client_id=client_id,
        active_page="profitability",
    )


@profitability_bp.route("/api/profitability/filter-options")
def api_profitability_filter_options():
    return jsonify({"account_managers": [], "dc_codes": [], "service_types": []})


@profitability_bp.route("/api/profitability")
def api_profitability():
    return jsonify({"by_customer": [], "by_dc": [], "by_service_type": [], "totals": {}})


@profitability_bp.route("/api/profitability/<int:client_id>")
def api_profitability_customer(client_id):
    return jsonify({"services": [], "summary": {}})
