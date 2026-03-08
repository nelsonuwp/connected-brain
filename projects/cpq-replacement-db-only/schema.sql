-- =============================================================================
-- CPQ Replacement — Supabase (Postgres) Schema
-- Version: POC / 2026-03-08
-- Scope: Server pricing (MH/DH unified as Hosting), DC availability,
--        component relationships. Firewalls, switches, colo: deferred.
--
-- FX convention: all rates = units of foreign currency per 1 CAD (CAD is root)
--   CAD → foreign : cad_amount × rate
--   Foreign → CAD : foreign_amount ÷ rate
--   Example: USD rate 1.3651 → $1,000 CAD × 1.3651 = $1,365.10 USD
--
-- Restore: psql -d <dbname> -f schema.sql
-- =============================================================================


-- =============================================================================
-- LAYER 0 — Lookup Tables
-- =============================================================================

CREATE TABLE currencies (
    currency_code   CHAR(3)      PRIMARY KEY,
    currency_name   TEXT         NOT NULL,
    symbol          TEXT         NOT NULL,
    is_base         BOOLEAN      NOT NULL DEFAULT false,
    CONSTRAINT chk_one_base CHECK (true)  -- enforced via application; only CAD has is_base=true
);

COMMENT ON TABLE currencies IS 'ISO 4217 currencies in use. CAD is root (is_base=true); never appears as a target in fx_rates.';
COMMENT ON COLUMN currencies.is_base IS 'True for CAD only. Base currency has implicit rate of 1; stored only here, not in fx_rates.';

-- Seed: run immediately after CREATE
INSERT INTO currencies (currency_code, currency_name, symbol, is_base) VALUES
    ('CAD', 'Canadian Dollar',  '$',  true),
    ('USD', 'US Dollar',        '$',  false),
    ('GBP', 'British Pound',    '£',  false),
    ('EUR', 'Euro',             '€',  false);


-- -----------------------------------------------------------------------------

CREATE TABLE fx_rates (
    id                      BIGSERIAL    PRIMARY KEY,
    currency_code           CHAR(3)      NOT NULL REFERENCES currencies(currency_code),
    rate_type               TEXT         NOT NULL,   -- 'ocean' | 'spot' | 'budget'
    rate_date               DATE         NOT NULL,
    rate                    NUMERIC(12,6) NOT NULL,  -- units of foreign per 1 CAD
    cad_pricing_rebased     BOOLEAN      NOT NULL DEFAULT false,
    confirmed_override      BOOLEAN      NOT NULL DEFAULT false,
    notes                   TEXT,
    created_at              TIMESTAMPTZ  NOT NULL DEFAULT now(),
    CONSTRAINT uq_fx_rate   UNIQUE (currency_code, rate_type, rate_date),
    CONSTRAINT chk_rate_pos CHECK (rate > 0),
    CONSTRAINT chk_rate_type CHECK (rate_type IN ('ocean', 'spot', 'budget')),
    CONSTRAINT chk_not_cad  CHECK (currency_code <> 'CAD')
);

COMMENT ON TABLE fx_rates IS 'Finance-maintained FX rates. Append-only — never update rows, always insert new. Rate = units of foreign currency per 1 CAD.';
COMMENT ON COLUMN fx_rates.rate IS 'Units of foreign currency per 1 CAD. Example: USD 1.3651 means 1 CAD = 1.3651 USD.';
COMMENT ON COLUMN fx_rates.rate_type IS 'ocean = locked rate for customer quotes. spot = current market for financial model. budget = internal planning rate for CapEx CAD derivation.';
COMMENT ON COLUMN fx_rates.cad_pricing_rebased IS 'Set to true when finance intentionally updates CAD prices in product_pricing in response to this rate change. Audit trail for repricing events.';
COMMENT ON COLUMN fx_rates.confirmed_override IS 'Set to true when a new budget rate differs from the prior rate by >10% and finance explicitly confirms the change is correct.';

CREATE INDEX idx_fx_rates_lookup ON fx_rates (currency_code, rate_type, rate_date DESC);


-- -----------------------------------------------------------------------------

CREATE TABLE product_types (
    type_code   TEXT    PRIMARY KEY,
    type_label  TEXT    NOT NULL,
    parent_code TEXT    REFERENCES product_types(type_code),
    level       TEXT    NOT NULL,
    CONSTRAINT chk_level CHECK (level IN ('TLS', 'Component', 'Both'))
);

COMMENT ON TABLE product_types IS 'Self-referencing product type hierarchy. Example: nvme → drive → storage_component.';
COMMENT ON COLUMN product_types.level IS 'TLS = top-level sellable. Component = goes into something. Both = can be either.';

INSERT INTO product_types (type_code, type_label, parent_code, level) VALUES
    -- TLS roots
    ('server',              'Server',                   NULL,               'TLS'),
    ('colocation',          'Colocation',               NULL,               'TLS'),
    ('firewall',            'Firewall',                 NULL,               'TLS'),
    ('switch',              'Network Switch',           NULL,               'TLS'),
    -- Component roots
    ('hardware_component',  'Hardware Component',       NULL,               'Component'),
    ('software',            'Software',                 NULL,               'Component'),
    ('network_component',   'Network Component',        NULL,               'Component'),
    -- Hardware subtypes
    ('cpu',                 'CPU / Processor',          'hardware_component', 'Component'),
    ('ram',                 'RAM',                      'hardware_component', 'Component'),
    ('storage_component',   'Storage',                  'hardware_component', 'Component'),
    ('drive',               'Drive',                    'storage_component',  'Component'),
    ('ssd',                 'SSD',                      'drive',              'Component'),
    ('nvme',                'NVMe',                     'drive',              'Component'),
    ('hdd',                 'HDD',                      'drive',              'Component'),
    ('sas',                 'SAS Drive',                'drive',              'Component'),
    ('psu',                 'Power Supply Unit',        'hardware_component', 'Component'),
    ('nic',                 'Network Interface Card',   'hardware_component', 'Component'),
    ('chassis',             'Chassis',                  'hardware_component', 'Component'),
    -- Software subtypes
    ('os',                  'Operating System',         'software',          'Component'),
    ('sql_server',          'SQL Server License',       'software',          'Component'),
    ('vmware',              'VMware License',           'software',          'Component'),
    ('backup_software',     'Backup Software',          'software',          'Component'),
    ('monitoring',          'Monitoring',               'software',          'Component'),
    ('remote_access',       'Remote Access',            'software',          'Component'),
    ('control_panel',       'Control Panel',            'software',          'Component'),
    ('ssl',                 'SSL Certificate',          'software',          'Component'),
    -- Network
    ('ipv4',                'IPv4 Address Block',       'network_component', 'Component'),
    ('bandwidth',           'Bandwidth',                'network_component', 'Component'),
    ('connectivity',        'Connectivity / Cross-Connect', 'network_component', 'Component'),
    -- Managed services (add-ons, TLS or component depending on context)
    ('managed_service',     'Managed Service',          NULL,               'Both'),
    ('backup_service',      'Managed Backup',           'managed_service',  'Both');


-- -----------------------------------------------------------------------------

CREATE TABLE data_centers (
    dc_code             CHAR(3)     PRIMARY KEY,
    dc_name             TEXT        NOT NULL,
    city                TEXT        NOT NULL,
    country             TEXT        NOT NULL,
    native_currency     CHAR(3)     NOT NULL REFERENCES currencies(currency_code),
    is_active           BOOLEAN     NOT NULL DEFAULT true,
    notes               TEXT
);

COMMENT ON TABLE data_centers IS '6 active data centers for server hosting. Colo available at MIA and POR only.';
COMMENT ON COLUMN data_centers.native_currency IS 'Currency in which this DC bills clients (USD for US DCs, CAD for TOR, GBP for POR).';

INSERT INTO data_centers (dc_code, dc_name, city, country, native_currency) VALUES
    ('ATL', 'Atlanta',          'Atlanta',   'US', 'USD'),
    ('MIA', 'Miami',            'Miami',     'US', 'USD'),
    ('LAX', 'Los Angeles',      'Los Angeles','US','USD'),
    ('IAD', 'Washington DC',    'Ashburn',   'US', 'USD'),
    ('TOR', 'Toronto',          'Toronto',   'CA', 'CAD'),
    ('POR', 'Portsmouth',       'Portsmouth','UK', 'GBP');


-- =============================================================================
-- LAYER 1 — Product Catalog
-- =============================================================================

CREATE TABLE product_catalog (
    id                       BIGSERIAL    PRIMARY KEY,
    fusion_id                TEXT         UNIQUE,           -- external anchor; TEMP-xxx for new SKUs
    sku_name                 TEXT         NOT NULL,
    sku_nickname             TEXT,
    product_type_code        TEXT         NOT NULL REFERENCES product_types(type_code),
    level                    TEXT         NOT NULL,
    release_date             DATE,
    end_of_sale_date         DATE,
    end_of_support_date      DATE,
    end_of_service_life_date DATE,
    vendor                   TEXT,
    is_active                BOOLEAN      NOT NULL DEFAULT true,
    notes                    TEXT,
    search_keywords          TEXT,
    created_at               TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at               TIMESTAMPTZ  NOT NULL DEFAULT now(),
    CONSTRAINT chk_level     CHECK (level IN ('TLS', 'Component'))
);

COMMENT ON TABLE product_catalog IS 'Master product list. fusion_id is the join key to Salesforce, billing, and all internal systems. BIGSERIAL id is the internal FK used by all other tables.';
COMMENT ON COLUMN product_catalog.fusion_id IS 'External system key. Nullable during POC for products not yet formally released (TEMP- placeholders tracked in pending_fusion_id). Must be populated before production go-live.';
COMMENT ON COLUMN product_catalog.level IS 'TLS = top-level sellable product. Component = goes into a server or service.';
COMMENT ON COLUMN product_catalog.is_active IS 'Soft-delete flag. Never DELETE rows — set is_active = false. Keeps history and prevents FK breakage.';

CREATE INDEX idx_product_catalog_fusion ON product_catalog (fusion_id) WHERE fusion_id IS NOT NULL;
CREATE INDEX idx_product_catalog_type   ON product_catalog (product_type_code);
CREATE INDEX idx_product_catalog_active ON product_catalog (is_active) WHERE is_active = true;

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_product_catalog_updated_at
    BEFORE UPDATE ON product_catalog
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();


-- =============================================================================
-- LAYER 2 — Type-Specific Specs (1:1 with product_catalog)
-- =============================================================================

CREATE TABLE server_specs (
    product_id              BIGINT       PRIMARY KEY REFERENCES product_catalog(id) ON DELETE RESTRICT,
    processor_sockets       SMALLINT,
    drive_bays              SMALLINT,
    default_cpu_qty         SMALLINT,
    default_drive_qty       SMALLINT,
    is_vhost                BOOLEAN      NOT NULL DEFAULT false,
    is_promo                BOOLEAN      NOT NULL DEFAULT false,
    min_contract_months     SMALLINT,    -- NULL = no minimum; 12 for promo servers
    allow_customization     BOOLEAN      NOT NULL DEFAULT true,
    notes                   TEXT
);

COMMENT ON TABLE server_specs IS '1:1 with product_catalog for TLS server products.';
COMMENT ON COLUMN server_specs.is_promo IS 'Promo servers: min 12-month contract, new clients only, no CPU/RAM changes.';
COMMENT ON COLUMN server_specs.min_contract_months IS 'NULL = no minimum. Promo servers = 12. Enforced by application layer.';
COMMENT ON COLUMN server_specs.allow_customization IS 'False for promo servers (no CPU/RAM changes). True for all others.';


-- -----------------------------------------------------------------------------

CREATE TABLE component_specs (
    product_id              BIGINT       PRIMARY KEY REFERENCES product_catalog(id) ON DELETE RESTRICT,
    -- CPU
    cores                   SMALLINT,
    threads                 SMALLINT,
    clock_ghz               NUMERIC(5,2),
    -- RAM
    ram_gb                  SMALLINT,
    -- Drive
    drive_capacity_tb       NUMERIC(8,3),
    drive_type              TEXT,        -- 'SSD' | 'NVMe' | 'HDD' | 'SAS'
    -- Shared
    watts                   SMALLINT,
    form_factor             TEXT,
    CONSTRAINT chk_drive_type CHECK (drive_type IN ('SSD', 'NVMe', 'HDD', 'SAS') OR drive_type IS NULL)
);

COMMENT ON TABLE component_specs IS '1:1 with product_catalog for Component products (CPU, RAM, Drive, PSU, NIC). Sparse columns — only relevant fields populated per component type.';
COMMENT ON COLUMN component_specs.drive_type IS 'For drive components: SSD | NVMe | HDD | SAS. NULL for non-drive components.';


-- =============================================================================
-- LAYER 3 — Pricing
-- =============================================================================

CREATE TABLE product_pricing (
    id                  BIGSERIAL    PRIMARY KEY,
    product_id          BIGINT       NOT NULL REFERENCES product_catalog(id),
    currency_code       CHAR(3)      NOT NULL REFERENCES currencies(currency_code),
    term_months         SMALLINT     NOT NULL,   -- 0 = month-to-month, 12, 24, 36
    mrc                 NUMERIC(12,2),
    nrc                 NUMERIC(12,2),
    pricing_model       TEXT         NOT NULL DEFAULT 'flat',
    effective_from      DATE,
    notes               TEXT,
    CONSTRAINT uq_pricing UNIQUE (product_id, currency_code, term_months),
    CONSTRAINT chk_term   CHECK (term_months IN (0, 12, 24, 36)),
    CONSTRAINT chk_model  CHECK (pricing_model IN ('flat', 'per_core', 'per_gb', 'per_unit'))
);

COMMENT ON TABLE product_pricing IS 'Customer-facing pricing. One row per product × currency × contract term. ~1,200 rows for server POC.';
COMMENT ON COLUMN product_pricing.term_months IS '0 = month-to-month. 12 / 24 / 36 = annual contract terms.';
COMMENT ON COLUMN product_pricing.mrc IS 'Monthly Recurring Charge in the specified currency. Flat rate per term — NOT a multiplier.';
COMMENT ON COLUMN product_pricing.nrc IS 'Non-Recurring Charge (one-time setup fee). NULL or 0 means no setup fee.';
COMMENT ON COLUMN product_pricing.pricing_model IS 'flat = fixed MRC regardless of quantity. per_core = VMware (rate × licensed_core_count). per_gb = storage overages. per_unit = per-IP, per-connection, etc.';
COMMENT ON COLUMN product_pricing.effective_from IS 'Date this pricing row became effective. NULL = original seed data with no specific effective date.';

CREATE INDEX idx_pricing_product   ON product_pricing (product_id);
CREATE INDEX idx_pricing_lookup    ON product_pricing (product_id, currency_code, term_months);


-- =============================================================================
-- LAYER 4 — CapEx (Time-Series Cost Snapshots)
-- =============================================================================

CREATE TABLE product_capex (
    id                  BIGSERIAL    PRIMARY KEY,
    product_id          BIGINT       NOT NULL REFERENCES product_catalog(id),
    procured_price      NUMERIC(12,2) NOT NULL,
    procured_currency   CHAR(3)      NOT NULL REFERENCES currencies(currency_code),
    procured_date       DATE         NOT NULL,
    use_as_baseline     BOOLEAN      NOT NULL DEFAULT true,
    residual_pct_12m    NUMERIC(5,4),    -- residual value at 12 months (0.85 = 85%)
    residual_pct_24m    NUMERIC(5,4),
    notes               TEXT,
    created_at          TIMESTAMPTZ  NOT NULL DEFAULT now()
);

COMMENT ON TABLE product_capex IS 'Hardware procurement cost tracking. One row per procurement batch. CAD equivalent derived at query time via LATERAL join to fx_rates (budget rate).';
COMMENT ON COLUMN product_capex.use_as_baseline IS 'Financial model uses: SELECT * FROM product_capex WHERE product_id = ? AND use_as_baseline = true AND procured_date <= quote_date ORDER BY procured_date DESC LIMIT 1. Set false for discounted or non-representative batches.';
COMMENT ON COLUMN product_capex.procured_price IS 'Hardware acquisition cost in procured_currency. NOT billed to customers.';
COMMENT ON COLUMN product_capex.residual_pct_12m IS 'Residual value percentage at 12 months. Example: 0.85 = retains 85% of original value.';

CREATE INDEX idx_capex_product ON product_capex (product_id, procured_date DESC);

-- Helper view: CAD-equivalent CapEx using most recent budget rate on or before procurement date
-- Usage: SELECT * FROM v_product_capex_cad WHERE product_id = ?
CREATE OR REPLACE VIEW v_product_capex_cad AS
SELECT
    pc.id,
    pc.product_id,
    pc.procured_price,
    pc.procured_currency,
    pc.procured_date,
    pc.use_as_baseline,
    pc.residual_pct_12m,
    pc.residual_pct_24m,
    CASE
        WHEN pc.procured_currency = 'CAD' THEN pc.procured_price
        ELSE pc.procured_price / fx.rate
    END AS procured_price_cad,
    fx.rate AS fx_budget_rate_used,
    fx.rate_date AS fx_rate_date
FROM product_capex pc
LEFT JOIN LATERAL (
    SELECT rate, rate_date
    FROM fx_rates
    WHERE currency_code = pc.procured_currency
      AND rate_type = 'budget'
      AND rate_date <= pc.procured_date
    ORDER BY rate_date DESC
    LIMIT 1
) fx ON true;

COMMENT ON VIEW v_product_capex_cad IS 'CAD equivalent of each CapEx row, derived at query time from the most recent budget FX rate on or before the procurement date.';


-- =============================================================================
-- LAYER 5 — Relationships
-- =============================================================================

CREATE TABLE server_dc_availability (
    server_product_id   BIGINT   NOT NULL REFERENCES product_catalog(id),
    dc_code             CHAR(3)  NOT NULL REFERENCES data_centers(dc_code),
    PRIMARY KEY (server_product_id, dc_code)
);

COMMENT ON TABLE server_dc_availability IS 'Which servers are available at which data centers. 88 rows from CPQ v28.';


-- -----------------------------------------------------------------------------

CREATE TABLE server_default_components (
    id                      BIGSERIAL   PRIMARY KEY,
    server_product_id       BIGINT      NOT NULL REFERENCES product_catalog(id),
    component_product_id    BIGINT      NOT NULL REFERENCES product_catalog(id),
    component_type          TEXT        NOT NULL,   -- 'cpu' | 'ram' | 'drive' | 'psu' | 'nic' | etc.
    quantity                SMALLINT    NOT NULL DEFAULT 1,
    CONSTRAINT uq_default_component UNIQUE (server_product_id, component_product_id)
);

COMMENT ON TABLE server_default_components IS 'Components included by default in each server SKU. 126 rows from CPQ v28.';
COMMENT ON COLUMN server_default_components.quantity IS 'How many of this component are included (e.g. 2 CPUs, 4 RAM sticks).';

CREATE INDEX idx_default_components_server ON server_default_components (server_product_id);


-- -----------------------------------------------------------------------------

CREATE TABLE server_selectable_options (
    id                      BIGSERIAL   PRIMARY KEY,
    server_product_id       BIGINT      NOT NULL REFERENCES product_catalog(id),
    component_product_id    BIGINT      NOT NULL REFERENCES product_catalog(id),
    category                TEXT        NOT NULL,   -- 'ram' | 'cpu' | 'drive' | 'nic' | 'os' | etc.
    is_included_default     BOOLEAN     NOT NULL DEFAULT false,
    display_order           SMALLINT,
    CONSTRAINT uq_selectable_option UNIQUE (server_product_id, component_product_id)
);

COMMENT ON TABLE server_selectable_options IS 'All components that can be selected or upgraded on each server. 655 rows from CPQ v28. This table is the source of truth for component compatibility — if a component is listed here for a server, it is valid for that server.';
COMMENT ON COLUMN server_selectable_options.is_included_default IS 'True if this option is included in the base server price. Mirrors server_default_components but allows the configurator to show defaults inline.';

CREATE INDEX idx_selectable_options_server ON server_selectable_options (server_product_id);
CREATE INDEX idx_selectable_options_category ON server_selectable_options (server_product_id, category);


-- =============================================================================
-- LAYER 6 — Financial Constants
-- =============================================================================

CREATE TABLE overhead_constants (
    key             TEXT         PRIMARY KEY,
    value           NUMERIC      NOT NULL,
    description     TEXT,
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT now()
);

COMMENT ON TABLE overhead_constants IS 'Global financial model constants. Finance-owned. ~12 rows.';

INSERT INTO overhead_constants (key, value, description) VALUES
    ('sga_pct',              0.082,  'SG&A as a percentage of revenue (8.2%)'),
    ('annual_cost_inflation',0.030,  'Annual cost inflation rate applied in IRR/NPV model (3.0%)'),
    ('software_markup_pct',  0.150,  'Markup applied over wholesale software cost for customer pricing (15%)'),
    ('ebit_poor_threshold',  -0.100, 'EBIT % below which a deal is flagged Poor (< -10%)'),
    ('ebit_moderate_target', 0.350,  'EBIT % for Moderate rating (35%)'),
    ('ebit_good_target',     0.375,  'EBIT % for Good rating (37.5%)'),
    ('ebit_strong_threshold',0.400,  'EBIT % at or above which a deal is rated Strong (>= 40%)'),
    ('capital_intensity_threshold', 0.500, 'Capital Intensity threshold (50%)');


-- -----------------------------------------------------------------------------

CREATE TABLE dc_cost_drivers (
    id              BIGSERIAL   PRIMARY KEY,
    dc_code         CHAR(3)     NOT NULL REFERENCES data_centers(dc_code),
    cost_category   TEXT        NOT NULL,
    amount          NUMERIC(12,4) NOT NULL,
    currency_code   CHAR(3)     NOT NULL REFERENCES currencies(currency_code),
    notes           TEXT,
    CONSTRAINT uq_dc_cost UNIQUE (dc_code, cost_category)
);

COMMENT ON TABLE dc_cost_drivers IS 'Internal per-DC cost overheads (power, rack, connectivity, etc.). 48 rows from CPQ v28. NOT billed to customers.';

CREATE INDEX idx_dc_cost_dc ON dc_cost_drivers (dc_code);


-- =============================================================================
-- LAYER 7 — POC Governance
-- =============================================================================

CREATE TABLE pending_fusion_id (
    id                  BIGSERIAL   PRIMARY KEY,
    product_id          BIGINT      NOT NULL REFERENCES product_catalog(id),
    placeholder_id      TEXT        NOT NULL,   -- e.g. 'TEMP-7.0-PRO'
    sku_name            TEXT        NOT NULL,
    reason              TEXT,                   -- why fusion_id is not yet assigned
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    resolved_at         TIMESTAMPTZ,
    resolved_fusion_id  TEXT
);

COMMENT ON TABLE pending_fusion_id IS 'Tracks product_catalog rows with TEMP- placeholder fusion_ids. Every placeholder must be resolved (real fusion_id assigned and this row deleted) before production go-live.';
COMMENT ON COLUMN pending_fusion_id.resolved_fusion_id IS 'Set when finance/product assigns the real fusion_id. Then: UPDATE product_catalog SET fusion_id = resolved_fusion_id WHERE id = product_id; DELETE FROM pending_fusion_id WHERE id = ?';

-- View: show all unresolved placeholders (must be empty before prod)
CREATE OR REPLACE VIEW v_pending_fusion_ids AS
SELECT
    p.id,
    p.placeholder_id,
    p.sku_name,
    p.reason,
    p.created_at,
    pc.is_active
FROM pending_fusion_id p
JOIN product_catalog pc ON pc.id = p.product_id
WHERE p.resolved_at IS NULL;

COMMENT ON VIEW v_pending_fusion_ids IS 'All unresolved TEMP- placeholders. Must return 0 rows before production go-live.';


-- =============================================================================
-- VALIDATION QUERIES (run after seed_data.sql to confirm correctness)
-- =============================================================================

-- See validation.md for full instructions. Quick checks:

-- 1. Product catalog loaded:
--    SELECT COUNT(*) FROM product_catalog WHERE level = 'TLS' AND is_active = true;
--    Expected: 18 (server SKUs)

-- 2. Pricing loaded:
--    SELECT COUNT(*) FROM product_pricing;
--    Expected: ~1,200 (18 servers × 3 currencies × 4 terms + component pricing)

-- 3. Primary validation — must match CPQ v28 exactly:
--    SELECT
--        pc.sku_name,
--        pp.currency_code,
--        pp.term_months,
--        pp.mrc,
--        pp.nrc
--    FROM product_catalog pc
--    JOIN product_pricing pp ON pp.product_id = pc.id
--    JOIN server_dc_availability sda ON sda.server_product_id = pc.id
--    WHERE pc.sku_name ILIKE '%Pro Series 6.0%'
--      AND sda.dc_code = 'TOR'
--      AND pp.currency_code = 'CAD'
--      AND pp.term_months = 36;

-- =============================================================================
-- END OF SCHEMA
-- =============================================================================
