CREATE DATABASE fqdb_nyc_taxi
ENGINE = PostgreSQL('host.docker.internal:5432', 'nyc_taxi', 'postgres', 'postgres', 'public', 0);
