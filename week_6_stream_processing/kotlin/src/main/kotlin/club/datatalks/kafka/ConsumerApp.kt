package club.datatalks.kafka

import club.datatalks.kafka.dto.RideDTO
import club.datatalks.kafka.infrastructure.KafkaJsonConsumer
import org.apache.kafka.clients.consumer.ConsumerRecords
import java.time.Duration


fun main() {
    val kafkaTopic = "rides"

    logger.info { "Starting Kafka Consumer binding on Topic='${kafkaTopic}'..." }
    val kafkaJsonConsumer = KafkaJsonConsumer<RideDTO>()
    while (true) {
        val records: ConsumerRecords<String, RideDTO> = kafkaJsonConsumer.subscribeTo(
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
