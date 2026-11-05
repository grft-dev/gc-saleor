"""Catalog operations exposed by Graftcode Gateway.

One row is slug|name|sku|price|currency. The amount uses a dot and two decimal places.
A missing product is an empty string. An empty catalog is an empty list.
"""

from catalog_store import _fetch_product, _fetch_products


class ProductCatalog:
    @staticmethod
    def get_products() -> list[str]:
        return _fetch_products()

    @staticmethod
    def get_product(slug: str) -> str:
        return _fetch_product(slug)
