# Builder stage
FROM python:3.9 AS builder

ADD pyproject.toml pdm.lock README.md /airflow/
WORKDIR /airflow

RUN pip install -U pip setuptools wheel && \
    pip install pdm && \
    mkdir __pypackages__ && \
    pdm sync --prod --no-editable

# Runner stage
FROM python:3.9-slim AS runner

ENV PYTHONPATH=/usr/local/lib/python/
COPY --from=builder /airflow/__pypackages__/3.9/lib /usr/local/lib/python/
COPY --from=builder /airflow/__pypackages__/3.9/bin/* /usr/local/bin/

WORKDIR /airflow/

ENTRYPOINT ["airflow"]