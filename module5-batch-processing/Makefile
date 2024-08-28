setup:
	@echo "Downloading gcs-connector into '$$(pwd)/jars/'"
	@wget https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-latest-hadoop2.jar -qP jars/
	@echo "Starting Spark in Docker..."
	@docker compose up -d
