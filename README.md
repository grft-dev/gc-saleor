# Saleor catalog on Graftcode

Graftcode Gateway loads `graft/saleor-catalog` and an external client calls `ProductCatalog`. The catalog read is the product. Django, GraphQL, Celery, Redis, checkout, payments, and webhooks are gone, because nothing on this path calls them.

The price in Saleor lives on a variant listing in a channel. This graft stores the current row the read needs: product name, default-variant SKU, and the USD channel price. The PLN channel is not in the seed.

## Exposed public surface

Module:

- `./saleor-catalog` (`pyproject.toml` name `saleor-catalog`)

Type and methods:

- `product_catalog.ProductCatalog`
  - `get_products() -> list[str]`
  - `get_product(slug: str) -> str`

`catalog_store` is not on the allowlist. The same names are in [graft/graft-method-allowlist.json](graft/graft-method-allowlist.json) and the image `CMD`.

One row is `slug|name|sku|price|currency`. The amount uses a dot and two decimal places. A missing product is `""`. An empty catalog is an empty list. Rows are ordered by slug, so the first seeded name is `Plimsolls`.

```text
blue-plimsolls|Plimsolls|818223583|75.00|USD
dash-force|Dash Force|618223581|90.00|USD
grey-hoodie|Hoodie|HD-GR-S|44.99|USD
```

`Hoodie` is the product name on slug `grey-hoodie`. Public methods are ordinary `def` calls. This slice reads through synchronous `psycopg`, so there is no sync-over-async helper.

This demo starts the stack without `GG_PROJECT_KEY`.

## 1) Start the graft stack

From `ports/gc-saleor`:

```powershell
docker compose -f docker-compose.graft.yml up --build -d
```

Ports:

- `8096` Gateway (WebSocket)
- `8097` Graft Vision
- `5434` Postgres (seeded catalog)

WebSocket endpoint for clients:

- `ws://localhost:8096/ws`

Graft Vision:

- `http://localhost:8097`

## 2) Install the generated client

After the container logs `pip install`, use the index and package id printed there. Open `http://localhost:8097` for Graft Vision.

The ids below are an example from one generation. Without a `GG_PROJECT_KEY` linked to your Graftcode account, every generation gets a new suffix and a new `https://grft.dev/simple/<guid>__free` index. With that key the id stays stable.

```powershell
python -m pip install --extra-index-url https://grft.dev/simple/68fc0af6-bc84-4744-bc81-c7450f0d5c08__free graft-pypi-saleor-catalog-hashid-dqtax6==1.0.0
```

PyPI will not replace an existing `1.0.0` when the package id stays the same. When the hash changes, install the new id from the index in that log. When the hash stays and the host surface changed, remove the cached `1.0.0` and install again from that same index.

`name` in the runtime config is the graft name from the generated `GraftConfig` (`graft_pypi_saleor_catalog`). The installable distribution adds `hashid` and the suffix.

```powershell
$env:GRAFTCODE_CONFIG_PYPI_SALEOR_CATALOG = "name=graft_pypi_saleor_catalog; runtime=python; modules=saleor-catalog; host=ws://localhost:8096/ws; stateless=true"
```

```python
from graft_pypi_saleor_catalog_dqtax6.product_catalog import ProductCatalog
from graft_pypi_saleor_catalog_dqtax6.graft_config import GraftConfig

GraftConfig.host = "ws://localhost:8096/ws"
GraftConfig.stateless = True
```

Replace `dqtax6` when the log prints a new suffix.

## 3) Run the external verifier

The verifier lives outside this repository, in `gc-saleor-graft-e2e` next to `ports/`. It calls `get_products` and `get_product` against the seed.

```powershell
$env:GRAFTCODE_CONFIG_PYPI_SALEOR_CATALOG = "name=graft_pypi_saleor_catalog; runtime=python; modules=saleor-catalog; host=ws://localhost:8096/ws; stateless=true"
python C:\Coding\Marketing\gc-saleor-graft-e2e\verify.py
```

## 4) Stop

```powershell
docker compose -f docker-compose.graft.yml down
```

## Troubleshooting

- The install command takes its index from the container log. There is no fixed feed URL. Without a project key, each start prints a new index. If install fails, restart the host and use the URL from that log.
- If port `8096` is occupied, change the published ports in `docker-compose.graft.yml` and point the client host at the new WebSocket URL.
