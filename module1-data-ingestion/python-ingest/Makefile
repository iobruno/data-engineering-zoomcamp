.PHONY: run docker-image docker-run

IMG_NAME := iobruno/ntlcli

docker-image:
	@docker build -t $(IMG_NAME) . --no-cache

docker-run:
	@docker run -d --rm \
		-e DB_HOST=host.docker.internal \
		-e DB_PORT=5432 \
		-e DB_NAME=nyc_taxi \
		-e DB_USERNAME=postgres \
		-e DB_PASSWORD=postgres \
		--name ntlcli \
		iobruno/ntlcli
