package club.datatalks.kafka

import club.datatalks.kafka.infrastructure.KafkaJsonConsumer
import club.datatalks.kafka.infrastructure.KafkaSerializable
import mu.KotlinLogging
import java.time.Duration

abstract class AbstractKafkaJsonConsumer<T>(
    private val topic: String,
    private val consumerGroup: String? = null,
    private val deserializationClass: Class<T>
) where T: KafkaSerializable {

    private val logger = KotlinLogging.logger {}

    fun start() {
        logger.info { "Starting Kafka Consumer binding on Topic='${topic}'..." }
        val kafkaJsonConsumer: KafkaJsonConsumer<T> = KafkaJsonConsumer(deserializationClass)

        while (true) {
            val records = kafkaJsonConsumer.subscribeTo(
                topic = topic,
                pollingDuration = Duration.ofSeconds(5L),
                consumerGroup = consumerGroup
            )
            if (!records.isEmpty) {
                logger.info { "Fetching ${records.count()} records from from topic='${topic}'" }
                records.map {
                    val message: T = it.value()
                    println(message)
                }
                logger.info { "Committing messages" }
                kafkaJsonConsumer.commit()
            } else {
                logger.info { "Still polling..." }
            }
        }
    }

}
