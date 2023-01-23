FROM python:3.11

WORKDIR /app

ADD requirements.txt requirements.txt
ADD app.yml app.yml
ADD df_persistence.py df_persistence.py
ADD pg_ingest.py pg_ingest.py

RUN pip install -r requirements.txt

ENV DATABASE_USERNAME=postgres
ENV DATABASE_PASSWORD=postgres
ENV DATABASE_HOST=postgres
ENV DATABASE_PORT=5432
ENV DATABASE_NAME=ny_taxi

ENTRYPOINT ["python", "pg_ingest.py", "-zyg"]
