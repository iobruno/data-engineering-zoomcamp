.PHONY: dirs setup full-setup minimal-setup

setup: minimal-setup

full-setup: dirs
	@docker-compose -f docker-compose.complex.yml up -d

minimal-setup: dirs
	@docker-compose -f docker-compose.simple.yml up -d

dirs:
	@mkdir -p volumes/confluent-{single-broker,multi-broker}/{zk-data,zk-txn-logs}
	@mkdir -p volumes/confluent-single-broker/kafka_0
	@mkdir -p volumes/confluent-multi-broker/kafka_{0,1,2}
