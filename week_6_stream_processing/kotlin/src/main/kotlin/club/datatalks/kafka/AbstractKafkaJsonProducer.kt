package club.datatalks.kafka

import club.datatalks.kafka.infrastructure.KafkaJsonProducer
import club.datatalks.kafka.infrastructure.KafkaSerializable
import mu.KotlinLogging
import java.io.BufferedReader
import java.nio.file.Files
import java.nio.file.Path
import kotlin.io.path.notExists
import kotlin.system.exitProcess

abstract class AbstractKafkaJsonProducer<T : KafkaSerializable> constructor(private val topic: String) {

    private val logger = KotlinLogging.logger {}

    fun fromCsv(filepath: Path, csvReaderFunction: (BufferedReader, Boolean) -> Sequence<T>) {
        logger.info { "Attempting to fetch CSV file..." }
        if (filepath.notExists()) {
            logger.error { "Could not load CSV. File not found!" }
            exitProcess(-1)
        }

        logger.info { "Deserializing CSV into a Data Class..." }
        val reader = Files.newBufferedReader(filepath)!!
        val records: Sequence<T> = csvReaderFunction(reader, true)

        logger.info { "Preparing to push messages to Kafka (topic='${topic}')" }
        val kafkaJsonProducer = KafkaJsonProducer<T>()
        val futures = kafkaJsonProducer.push(records, topic = topic)

        logger.info { "Awaiting for all messages to be successfully sent..." }
        futures.forEach { it.get() }

        logger.info { "All done!" }
    }

}
