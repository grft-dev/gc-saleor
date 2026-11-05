"""Database reads for the catalog graft.

This module stays off the Gateway allowlist. ProductCatalog is the only public type.
"""

import os
from decimal import Decimal

import psycopg

_MISSING_DSN = "Missing SALEOR_CATALOG_DSN environment variable."

_LIST_SQL = """
    SELECT slug, name, sku, price, currency
    FROM catalog_product
    ORDER BY slug
"""

_ONE_SQL = """
    SELECT slug, name, sku, price, currency
    FROM catalog_product
    WHERE slug = %s
"""


def _dsn() -> str:
    value = os.environ.get("SALEOR_CATALOG_DSN", "").strip()
    if not value:
        raise ValueError(_MISSING_DSN)
    return value


def _format_row(slug: str, name: str, sku: str, price: Decimal, currency: str) -> str:
    amount = f"{price:.2f}"
    return "|".join((slug, name, sku, amount, currency.strip()))


def _fetch_products() -> list[str]:
    with psycopg.connect(_dsn()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(_LIST_SQL)
            return [_format_row(*row) for row in cursor.fetchall()]


def _fetch_product(slug: str) -> str:
    with psycopg.connect(_dsn()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(_ONE_SQL, (slug,))
            row = cursor.fetchone()
            return "" if row is None else _format_row(*row)
