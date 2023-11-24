# Builder stage
FROM python:3.11.6-slim AS builder

## COPY project files
ADD pyproject.toml pdm.lock /app/
WORKDIR /app/

## Install dependencies
RUN pip install -U pip setuptools wheel && \
    pip install pdm && \
    mkdir -p __pypackages__ && \
    pdm sync --prod --no-editable

# Runner stage
FROM python:3.11.6-slim AS runner

ENV DATABASE_USERNAME=postgres
ENV DATABASE_PASSWORD=postgres
ENV DATABASE_HOST=postgres
ENV DATABASE_PORT=5432
ENV DATABASE_NAME=nyc_taxi

ENV PYTHONPATH=/app/pkgs
COPY --from=builder /app/__pypackages__/3.11/lib /app/pkgs
COPY pg_ingest.py app.yml README.md /app/

ENTRYPOINT ["python", "/app/pg_ingest.py", "-zyg"]