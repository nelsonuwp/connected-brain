# CPQ Front-End

Internal Flask web app for Aptum's Configure-Price-Quote tool. Presents server
products with live pricing, default/allowed components, hardware costs,
wattage, FX-converted overhead, and editable cost drivers.

## What it does

A single-file Flask app (`app.py`) backed by two read-only data sources plus
one editable local JSON file:

| Data source | Access | What it provides |
|---|---|---|
| **Fusion PostgreSQL** | SSH tunnel → psycopg2 | Active datacenters, product catalog, pricebook (MRC/NRC), component templates |
| **MSSQL `DM_BusinessInsights`** | Direct → pymssql | Hardware costs (`ocean_sku_cost`), wattage (`hardware_watts`), FX rates (`dimCurrencyExchangeRates`) |
| **`cost_drivers.json`** | Local file | Per-DC overhead rates (power, network, support, SG&A %). Edited via `/settings` page |

The app is intended to run locally against the Aptum network — the SSH tunnel
target (`10.121.21.20` by default) is not reachable from the public internet,
so this container expects to be run on a host with access to that host.

### Routes

| Route | Purpose |
|---|---|
| `/` | Server catalog (filter by DC, currency, product line) |
| `/product/<id>` | Single-server configurator with hardware cost & overhead |
| `/settings` | Edit `cost_drivers.json` (overhead rates and SG&A %) |
| `/api/datacenters` | Active DCs from Fusion, merged with `cost_drivers.json` |
| `/api/servers` | Pricebook server list in display currency |
| `/api/product/<id>` | Single product metadata |
| `/api/product/<id>/config` | Full priced configuration (MRC/NRC/overhead/CapEx/wattage) |
| `/api/fx-rate?from=&to=` | FX rate lookup |
| `/api/settings/overhead` | GET/POST cost_drivers.json |

## Requirements

- Docker
- GNU `make`
- Network access to the SSH tunnel host and the MSSQL server
- Credentials for: Fusion SSH user, Fusion DB read-only user, MSSQL
  BusinessInsights read-only user

## Quick start

```bash
cp .env.sample .env
# fill in SSH_USER, SSH_PASS, FUSION_DB_PASS, MSSQL_BI_* values
make            # builds the image then runs the dev server
```

App will be at <http://localhost:5050>.

## Make targets

| Target | What it does |
|---|---|
| `make` (default) | `make build` then `make run` |
| `make build` | Build the `cpq-front-end` Docker image |
| `make run` | Run the dev server: Flask debug mode, auto-reload, source bind-mounted (edit `app.py` / `templates/` without rebuilding) |
| `make run-prod` | Run via gunicorn — no debug, no auto-reload, no source mount |
| `make shell` | Open a bash shell inside the running image (useful for poking at `psql`/`pymssql` connectivity) |
| `make clean` | Remove the image |

`make run` and `make run-prod` both publish port `5050` and load env from
`.env`. Settings page edits to `cost_drivers.json` are persisted via a bind
mount in both modes.

## `.env` reference

```bash
# SSH tunnel into Aptum network (required)
SSH_HOST=10.121.21.20
SSH_PORT=22
SSH_USER=
SSH_PASS=

# Fusion PostgreSQL (reached through the tunnel)
FUSION_DB_SERVER=db1.peer1.com
FUSION_DB_PORT=5432
FUSION_DB_NAME=fusion
FUSION_DB_USER=sb_readonly
FUSION_DB_PASS=

# MSSQL DM_BusinessInsights (direct connection)
MSSQL_BI_SERVER=
MSSQL_BI_NAME=DM_BusinessInsights
MSSQL_BI_USER=
MSSQL_BI_PASS=
```

The app will start without MSSQL credentials — hardware cost, wattage, and FX
features will simply return empty or `1.0`. It will **not** start without SSH
and Fusion credentials.

## Notes on data behaviour

- **DC list:** queried from Fusion `sb_datacenter`, then merged with
  `cost_drivers.json` for `native_currency` and overhead rates. If Fusion is
  unreachable, falls back to the JSON file alone.
- **Currency:** the pricebook is queried in the requested display currency
  first; if no rows exist, the app falls back to the DC's native currency and
  converts via the MSSQL FX table.
- **Cost drivers:** the `/settings` POST writes `cost_drivers.json` atomically
  (`.tmp` + `os.replace`) and reloads the in-memory cache. Validation enforces
  `0 ≤ sga_pct ≤ 1` and non-negative cost amounts.
- **Hardware cost:** server-level row in `ocean_sku_cost` (level=`TLS`) wins
  over component-sum when computing total CapEx.

## Files

```
app.py                  # Flask app, all routes, DB helpers, overhead calc
cost_drivers.json       # Editable: DC overhead rates + SG&A %
requirements.txt        # flask, dotenv, psycopg2-binary, sshtunnel, pymssql
templates/              # index.html, product.html, settings.html
cpq-data-flow.md        # How data flows from Fusion/MSSQL to the UI
cpq-quoting-flow.md     # Quoting/pricing logic reference
Dockerfile              # python:3.12-slim-bookworm base
Makefile                # build / run / run-prod / shell / clean
.env.sample             # Template for required environment variables
```
