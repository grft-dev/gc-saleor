FROM python:3.12-bookworm

WORKDIR /usr/app

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates curl libcap2-bin && \
    rm -rf /var/lib/apt/lists/*

COPY saleor-catalog /usr/app/saleor-catalog

RUN pip install --no-cache-dir /usr/app/saleor-catalog \
    && curl -fsSL -o gg.deb "https://github.com/grft-dev/graftcode-gateway/releases/latest/download/gg_linux_amd64.deb" \
    && dpkg -i gg.deb \
    && rm gg.deb

RUN groupadd -r appuser && useradd -r -g appuser appuser && chown -R appuser:appuser /usr/app
RUN setcap 'cap_net_bind_service=+ep' "$(command -v gg)"

USER appuser

EXPOSE 80
EXPOSE 81

CMD ["gg", "--modules", "./saleor-catalog", "--types", "product_catalog.ProductCatalog", "--methods", "get_products,get_product"]
