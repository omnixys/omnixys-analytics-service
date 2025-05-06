-- SQL-Schema für GentleKPI
-- Erstellt Tabellen für Kunden-, Transaktions-, Bestell- und Produkt-KPIs

CREATE TABLE IF NOT EXISTS customer_kpis (
    id UUID PRIMARY KEY USING INDEX TABLESPACE kpispace,
    user_id VARCHAR(64) NOT NULL,
    registered_at TIMESTAMP NOT NULL,
    deregistered_at TIMESTAMP
) TABLESPACE kpispace;

CREATE TABLE IF NOT EXISTS transaction_kpis (
    id UUID PRIMARY KEY USING INDEX TABLESPACE kpispace,
    user_id VARCHAR(64) NOT NULL,
    amount DOUBLE PRECISION NOT NULL,
    transaction_type VARCHAR(20) NOT NULL CHECK (transaction_type IN ('TRANSFER', 'PURCHASE')),
    created_at TIMESTAMP NOT NULL
) TABLESPACE kpispace;

CREATE TABLE IF NOT EXISTS order_kpis (
    id UUID PRIMARY KEY USING INDEX TABLESPACE kpispace,
    user_id VARCHAR(64) NOT NULL,
    total_price DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP NOT NULL
) TABLESPACE kpispace;

CREATE TABLE IF NOT EXISTS product_movement_kpis (
    id UUID PRIMARY KEY USING INDEX TABLESPACE kpispace,
    product_id VARCHAR(64) NOT NULL,
    movement_type VARCHAR(20) NOT NULL CHECK (movement_type IN ('PURCHASED', 'SOLD')),
    quantity INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL
) TABLESPACE kpispace;

-- Indexes
CREATE INDEX IF NOT EXISTS idx_customer_user_id ON customer_kpis(user_id);
CREATE INDEX IF NOT EXISTS idx_transaction_user_id ON transaction_kpis(user_id);
CREATE INDEX IF NOT EXISTS idx_order_user_id ON order_kpis(user_id);
CREATE INDEX IF NOT EXISTS idx_kpi_id ON product_movement_kpis(product_id);
