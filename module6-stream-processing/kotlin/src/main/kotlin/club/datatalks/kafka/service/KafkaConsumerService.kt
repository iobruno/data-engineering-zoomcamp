package club.datatalks.kafka.service

import club.datatalks.kafka.infrastructure.KafkaJsonConsumer
import club.datatalks.kafka.infrastructure.KafkaSerializable
import io.github.oshai.kotlinlogging.KotlinLogging

import java.time.Duration
import kotlin.reflect.KClass

class KafkaConsumerService<T>(
    private val topic: String,
    private val consumerGroup: String,
    private val deserializationClass: KClass<T>
) where T : KafkaSerializable {

    private val logger = KotlinLogging.logger {}

    companion object {
        const val POLLING_DURATION = 5L
    }

    fun start() {
        logger.info { "Starting Kafka Consumer binding on Topic='${topic}'..." }
        val kafkaJsonConsumer: KafkaJsonConsumer<T> = KafkaJsonConsumer(deserializationClass)

        while (true) {
            val records = kafkaJsonConsumer.subscribeTo(
                topic = topic,
                pollingDuration = Duration.ofSeconds(POLLING_DURATION),
                consumerGroup = consumerGroup
            )
            if (!records.isEmpty) {
                logger.info { "Fetching ${records.count()} records from from topic='${topic}'" }
                records.map {
                    val message: T = it.value()
                    logger.info { message }
                }
                logger.info { "Committing messages" }
                kafkaJsonConsumer.commit()
            } else {
                logger.info { "Still polling..." }
            }
        }
    }

}
