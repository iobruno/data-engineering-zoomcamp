# Builder stage
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1

RUN --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=README.md,target=README.md \
    uv pip install -r pyproject.toml --system

ADD analyses /dbt/analyses
ADD macros   /dbt/macros
ADD models   /dbt/models
ADD seeds    /dbt/seeds
ADD tests    /dbt/tests
ADD dbt_project.yml package-lock.yml packages.yml /dbt/
ADD profiles.tmpl.yml                             /dbt/profiles.yml

# Runner stage
FROM python:3.12-slim AS runner

ENV DBT_PROFILES_DIR=/dbt/
ENV DBT_REDSHIFT_HOST=
ENV DBT_REDSHIFT_DATABASE=
ENV DBT_REDSHIFT_SCHEMA=
ENV AWS_ACCESS_KEY_ID=
ENV AWS_SECRET_ACCESS_KEY=

COPY --from=builder /usr/local/lib/python3.12   /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin/*            /usr/local/bin/
COPY --from=builder /dbt                        /dbt

WORKDIR /dbt/

ENTRYPOINT ["sh", "-c", "dbt deps && dbt seed --target prod && dbt run --target prod"]