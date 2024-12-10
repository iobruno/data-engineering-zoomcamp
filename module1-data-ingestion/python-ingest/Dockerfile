# Builder stage
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=README.md,target=README.md \
    uv pip install . --system

ADD app /ntlcli/app/

# Runner stage
FROM python:3.12-slim AS runner

WORKDIR /ntlcli/

ENV PYTHONPATH=/ntlcli
COPY --from=builder /usr/local/lib/python3.12   /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin/*            /usr/local/bin/
COPY --from=builder /ntlcli/                    /ntlcli/
ADD pyproject.toml uv.lock datasets.yaml        /ntlcli/

ENTRYPOINT ["ntlcli", "ingest", "-zygf", "--use-polars"]