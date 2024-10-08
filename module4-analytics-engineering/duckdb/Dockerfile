# Builder stage
FROM python:3.12-slim AS builder

ADD pyproject.toml pdm.lock /app/
WORKDIR /app/

RUN pip install -U pip setuptools wheel && \
    pip install pdm && \
    mkdir -p __pypackages__ && \
    pdm sync --prod --no-self --no-editable

# Runner stage
FROM python:3.12-slim AS runner

ENV DBT_PROFILES_DIR=/dbt/
ENV DBT_DUCKDB_SOURCE_PARQUET_BASE_PATH=
ENV DBT_DUCKDB_TARGET_PATH=/tmp/dbt.duckdb
ENV GOOGLE_APPLICATION_CREDENTIALS=/secrets/gcp_credentials.json

ENV PYTHONPATH=/usr/local/lib/python/
COPY --from=builder /app/__pypackages__/3.12/lib /usr/local/lib/python/
COPY --from=builder /app/__pypackages__/3.12/bin /usr/local/bin

ADD analyses /dbt/analyses
ADD macros   /dbt/macros
ADD models   /dbt/models
ADD seeds    /dbt/seeds
ADD tests    /dbt/tests
ADD dbt_project.yml package-lock.yml packages.yml /dbt/
ADD profiles.tmpl.yml /dbt/profiles.yml

WORKDIR /dbt/

ENTRYPOINT ["sh", "-c", "dbt deps && dbt seed --target dev && dbt run --target dev"]