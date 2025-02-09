FROM apache/airflow:slim-2.10.4-python3.12

USER airflow

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
