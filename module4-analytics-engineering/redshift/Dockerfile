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
ENV DBT_REDSHIFT_HOST=
ENV DBT_REDSHIFT_DATABASE=
ENV DBT_REDSHIFT_SCHEMA=
ENV AWS_ACCESS_KEY_ID=
ENV AWS_SECRET_ACCESS_KEY=

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

ENTRYPOINT ["sh", "-c", "dbt deps && dbt seed --target prod && dbt run --target prod"]