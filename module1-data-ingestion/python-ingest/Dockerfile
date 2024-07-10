# Builder stage
FROM python:3.12-slim AS builder

ADD pyproject.toml pdm.lock /app/
WORKDIR /app/

RUN pip install -U pip setuptools wheel && \
    pip install pdm && \
    mkdir -p __pypackages__ && \
    pdm sync --prod --no-editable

# Runner stage
FROM python:3.12-slim AS runner

ENV DATABASE_HOST=
ENV DATABASE_PORT=
ENV DATABASE_USERNAME=
ENV DATABASE_PASSWORD=
ENV DATABASE_NAME=

ENV PYTHONPATH=/usr/local/lib/python/
COPY --from=builder /app/__pypackages__/3.12/lib /usr/local/lib/python/

ADD src /app/src/
ADD run.py datasets.yaml /app/

WORKDIR /app/

ENTRYPOINT ["python", "run.py", "-zygf", "--use-polars"]