# Builder stage
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /ntlcli

ENV UV_COMPILE_BYTECODE=1

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv pip install -r pyproject.toml --system

ADD app /ntlcli/app/

# Runner stage
FROM python:3.12-slim AS runner

COPY --from=builder /usr/local/lib/python3.12   /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin/*            /usr/local/bin/
COPY --from=builder /ntlcli/                    /ntlcli/
ADD pyproject.toml uv.lock datasets.yaml        /ntlcli/
ADD run.py                                      /ntlcli/

WORKDIR /ntlcli/

ENTRYPOINT ["python", "run.py", "ingest", "-zygf", "--use-polars"]
