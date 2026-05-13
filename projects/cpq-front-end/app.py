import os
import sys
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from sshtunnel import SSHTunnelForwarder

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

SSH_HOST = os.environ.get("SSH_HOST", "10.121.21.20")
SSH_PORT = int(os.environ.get("SSH_PORT", "22"))
SSH_USER = os.environ.get("SSH_USER", "")
SSH_PASSWORD = os.environ.get("SSH_PASS", "")

DB_REMOTE_HOST = os.environ.get("FUSION_DB_SERVER", "db1.peer1.com")
DB_REMOTE_PORT = int(os.environ.get("FUSION_DB_PORT", "5432"))
DB_NAME = os.environ.get("FUSION_DB_NAME", "fusion")
DB_USER = os.environ.get("FUSION_DB_USER", "sb_readonly")
DB_PASSWORD = os.environ.get("FUSION_DB_PASS", "")

app = Flask(__name__)

_tunnel = None
_conn = None


def get_conn():
    global _tunnel, _conn

    if _conn:
        try:
            _conn.cursor().execute("SELECT 1")
            return _conn
        except Exception:
            _conn = None

    if _tunnel and not _tunnel.is_active:
        _tunnel = None

    if not _tunnel:
        _tunnel = SSHTunnelForwarder(
            (SSH_HOST, SSH_PORT),
            ssh_username=SSH_USER,
            ssh_password=SSH_PASSWORD,
            remote_bind_address=(DB_REMOTE_HOST, DB_REMOTE_PORT),
        )
        _tunnel.start()

    _conn = psycopg2.connect(
        host="127.0.0.1",
        port=_tunnel.local_bind_port,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        gssencmode="disable",
        cursor_factory=RealDictCursor,
    )
    _conn.set_session(readonly=True, autocommit=True)
    return _conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/product-classes")
def product_classes():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, name FROM public.product_classes ORDER BY sort_order, name"
        )
        rows = [dict(r) for r in cur.fetchall()]
    return jsonify(rows)


@app.route("/api/products/<int:class_id>")
def products(class_id):
    from flask import request
    show_inactive = request.args.get("show_inactive", "false").lower() == "true"

    conn = get_conn()
    with conn.cursor() as cur:
        if show_inactive:
            cur.execute(
                """
                SELECT id, name, description, is_active, sku,
                       available_in_shop, sold_out, limited_availability,
                       release_date
                FROM public.product_catalog
                WHERE product_class = %s
                ORDER BY name
                """,
                (class_id,),
            )
        else:
            cur.execute(
                """
                SELECT id, name, description, is_active, sku,
                       available_in_shop, sold_out, limited_availability,
                       release_date
                FROM public.product_catalog
                WHERE product_class = %s AND is_active = true
                ORDER BY name
                """,
                (class_id,),
            )
        rows = [dict(r) for r in cur.fetchall()]
    return jsonify(rows)


if __name__ == "__main__":
    if not SSH_USER or not DB_PASSWORD:
        print("ERROR: SSH_USER or FUSION_DB_PASS not set", file=sys.stderr)
        sys.exit(1)
    app.run(debug=True, port=5050)
