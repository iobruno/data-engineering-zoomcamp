FROM python:3.10

WORKDIR /app

ADD pyproject.toml pyproject.toml
ADD poetry.lock poetry.lock
ADD app.yml app.yml
ADD pg_ingest.py pg_ingest.py

ENV DATABASE_USERNAME=postgres
ENV DATABASE_PASSWORD=postgres
ENV DATABASE_HOST=postgres
ENV DATABASE_PORT=5432
ENV DATABASE_NAME=ny_taxi
ENV POETRY_VIRTUALENVS_CREATE=false

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN $HOME/.local/bin/poetry install --without dev --no-root && \
    rm -Rf /root/.local && \
    rm -Rf /usr/share/doc/ &&  \
    rm -Rf /tmp/ && \
    rm -Rf /var/cache

ENTRYPOINT ["python", "pg_ingest.py", "-zyg"]