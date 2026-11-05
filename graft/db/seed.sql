CREATE TABLE IF NOT EXISTS catalog_product (
    slug text PRIMARY KEY,
    name text NOT NULL,
    sku text NOT NULL,
    price numeric(12, 2) NOT NULL,
    currency text NOT NULL
);

-- Current catalog row: product name, default-variant SKU, and the USD channel price.
-- Source: saleor/static/populatedb_data.json. The PLN channel stays out of this table.
INSERT INTO catalog_product (slug, name, sku, price, currency)
VALUES
    ('blue-plimsolls', 'Plimsolls', '818223583', 75.00, 'USD'),
    ('dash-force', 'Dash Force', '618223581', 90.00, 'USD'),
    ('grey-hoodie', 'Hoodie', 'HD-GR-S', 44.99, 'USD')
ON CONFLICT (slug) DO NOTHING;
