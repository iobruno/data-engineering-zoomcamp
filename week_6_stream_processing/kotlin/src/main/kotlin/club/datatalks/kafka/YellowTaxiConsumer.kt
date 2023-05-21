package club.datatalks.kafka

import club.datatalks.kafka.dto.YellowTaxiDTO
import club.datatalks.kafka.infrastructure.KafkaJsonConsumer
import java.time.Duration


fun main() {
    val kafkaTopic = "yellow_tripdata"

    logger.info { "Starting Kafka Consumer binding on Topic='${kafkaTopic}'..." }
    val kafkaJsonConsumer = KafkaJsonConsumer(YellowTaxiDTO::class.java)
    while (true) {
        val records = kafkaJsonConsumer.subscribeTo(
            topic = kafkaTopic,
            pollingDuration = Duration.ofSeconds(5L)
        )
        if (!records.isEmpty) {
            logger.info { "Fetching ${records.count()} records from from topic='${kafkaTopic}'" }
            records.map { println(it.value()) }
            logger.info { "Committing messages" }
            kafkaJsonConsumer.commit()
        } else {
            logger.info { "Still polling..." }
        }
    }

}
