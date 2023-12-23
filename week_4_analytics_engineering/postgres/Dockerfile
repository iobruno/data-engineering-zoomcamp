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

ENV DBT_POSTGRES_HOST=localhost
ENV DBT_POSTGRES_PORT=5432
ENV DBT_POSTGRES_DATABASE=
ENV DBT_POSTGRES_SCHEMA=
ENV DBT_POSTGRES_USER=
ENV DBT_POSTGRES_PASSWORD=

ENV PYTHONPATH=/app/pkgs
COPY --from=builder /app/__pypackages__/3.11/lib /app/pkgs
COPY --from=builder /app/__pypackages__/3.11/bin /usr/local/bin

ADD analyses /app/analyses
ADD macros /app/macros
ADD models /app/models
ADD seeds /app/seeds
ADD tests /app/tests
ADD dbt_project.yml package-lock.yml packages.yml /app/
ADD profiles.tmpl.yml /app/profiles.yml

WORKDIR /app/

ENTRYPOINT ["sh", "-c", "dbt deps && dbt seed --target prod && dbt run --target prod"]