-- Migration: create pricing_rules table for core-driven licensing

CREATE TABLE IF NOT EXISTS pricing_rules (
    id                    BIGSERIAL PRIMARY KEY,
    product_id            BIGINT    NOT NULL REFERENCES product_catalog(id),
    cost_driver           TEXT      NOT NULL,
    min_units_per_socket  SMALLINT,
    min_units_per_server  SMALLINT,
    unit_increment        SMALLINT,
    mrc_represents        TEXT      NOT NULL DEFAULT 'per_unit',
    notes                 TEXT,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_pricing_rule_product UNIQUE (product_id),
    CONSTRAINT chk_cost_driver CHECK (cost_driver IN (
        'licensed_cores', 'raw_cores', 'core_packs', 'vcpu_count', 'flat'
    )),
    CONSTRAINT chk_mrc_represents CHECK (mrc_represents IN (
        'per_unit', 'per_pack', 'per_tier_unit', 'flat_total'
    ))
);

COMMENT ON TABLE pricing_rules IS
  'Licensing math for core-driven products. One row per product defines how to compute billable units from server CPU config. '
  'product_pricing.mrc stores the unit price; this table says what a \"unit\" is.';
COMMENT ON COLUMN pricing_rules.cost_driver IS
  'licensed_cores = VMware (floored + rounded core count). '
  'raw_cores = SQL Server (physical core total). '
  'core_packs = Windows Server (2-core pack licensing). '
  'vcpu_count = RHEL for VMs (virtual CPUs). '
  'flat = no core driver (override default flat behavior).';
COMMENT ON COLUMN pricing_rules.min_units_per_socket IS
  'Floor per CPU socket. VMware: 16 (an 8-core CPU counts as 16). SQL: 4. Windows: 8. NULL = no floor.';
COMMENT ON COLUMN pricing_rules.min_units_per_server IS
  'Floor per server total. Windows: 16 (even a single 8-core socket counts as 16). NULL = no floor.';
COMMENT ON COLUMN pricing_rules.unit_increment IS
  'Round total up to nearest N. VMware/SQL/Windows: 2 (sold in 2-core increments). NULL = no rounding.';
COMMENT ON COLUMN pricing_rules.mrc_represents IS
  'per_unit = MRC is price per 1 core (VMware). '
  'per_pack = MRC is price per 2-core pack (SQL, Windows). '
  'per_tier_unit = MRC is price per vCPU at the selected tier (RHEL). '
  'flat_total = MRC is the total, no multiplication.';

CREATE INDEX IF NOT EXISTS idx_pricing_rules_product ON pricing_rules (product_id);

