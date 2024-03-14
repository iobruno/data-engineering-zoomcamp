export PGHOST=localhost
export PGPORT=4566
export PGUSER=root
export PGDATABASE=dev

# Seed trip data from the parquet file
seed-kafka() {
	./seed_kafka.py
}

# Seed trip data from the parquet file
stream-kafka() {
	./seed_kafka.py update
}

# TODO: Command to create ALL ddls.
# TODO: Command + script to send kafka updates.

# Starts the risingwave cluster
start-cluster() {
	docker-compose -f docker/docker-compose.yml up -d
}

# Stops the risingwave cluster
stop-cluster() {
	docker-compose -f docker/docker-compose.yml down
}

# Cleans the risingwave cluster
clean-cluster() {
	docker-compose -f docker/docker-compose.yml down -v
}

# Starts the clickhouse client.
# You can run files like:
# clickhouse-client < file.sql
clickhouse-client() {
  docker exec -i clickhouse clickhouse-client
}

# Starts an interactive clickhouse session.
clickhouse-client-term() {
  docker exec -it clickhouse clickhouse-client
}