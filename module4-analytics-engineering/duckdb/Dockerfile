# Builder stage
FROM python:3.11-slim AS builder

ADD pyproject.toml pdm.lock /app/
WORKDIR /app/

RUN pip install -U pip setuptools wheel && \
    pip install pdm && \
    mkdir -p __pypackages__ && \
    pdm sync --prod --no-editable

# Runner stage
FROM python:3.11-slim AS runner

ENV DBT_DUCKDB_DIR=/dbt/
ENV DBT_DUCKDB_SOURCE_GCS_PATH=
ENV DBT_DUCKDB_TARGET_FILE_PATH=

ENV PYTHONPATH=/usr/local/lib/python/
COPY --from=builder /app/__pypackages__/3.11/lib /usr/local/lib/python/
COPY --from=builder /app/__pypackages__/3.11/bin /usr/local/bin

ADD analyses /dbt/analyses
ADD macros   /dbt/macros
ADD models   /dbt/models
ADD seeds    /dbt/seeds
ADD tests    /dbt/tests
ADD dbt_project.yml package-lock.yml packages.yml /dbt/
ADD profiles.tmpl.yml /dbt/profiles.yml

WORKDIR /dbt/

ENTRYPOINT ["sh", "-c", "dbt deps && dbt seed && dbt run"]