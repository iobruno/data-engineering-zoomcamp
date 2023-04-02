package club.datatalks.kafka

import club.datatalks.kafka.infrastructure.KafkaJsonConsumer
import mu.KotlinLogging
import java.time.Duration

abstract class AbstractKafkaJsonConsumer(
    private val topic: String,
    private val consumerGroup: String? = null,
    private val deserializationClass: Class<*>
) {

    private val logger = KotlinLogging.logger {}

    fun start() {
        logger.info { "Starting Kafka Consumer binding on Topic='${topic}'..." }
        val kafkaJsonConsumer: KafkaJsonConsumer<out Any> = KafkaJsonConsumer(deserializationClass)

        while (true) {
            val records = kafkaJsonConsumer.subscribeTo(
                topic = topic,
                pollingDuration = Duration.ofSeconds(5L),
                consumerGroup = consumerGroup
            )
            if (!records.isEmpty) {
                logger.info { "Fetching ${records.count()} records from from topic='${topic}'" }
                records.map {
                    val message = it.value()
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
