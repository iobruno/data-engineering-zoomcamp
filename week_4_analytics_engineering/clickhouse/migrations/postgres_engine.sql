CREATE DATABASE raw_pgdata
ENGINE = PostgreSQL('postgres:5432', 'nyc_taxi', 'postgres', 'postgres', 'raw_nyc_trip_record_data', 0);
