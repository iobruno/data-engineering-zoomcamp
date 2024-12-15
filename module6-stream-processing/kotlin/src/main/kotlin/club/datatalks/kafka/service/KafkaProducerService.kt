package club.datatalks.kafka.service

import club.datatalks.kafka.infrastructure.KafkaJsonProducer
import club.datatalks.kafka.infrastructure.KafkaSerializable
import io.github.oshai.kotlinlogging.KotlinLogging
import org.apache.kafka.clients.producer.RecordMetadata
import org.jetbrains.kotlinx.dataframe.DataFrame
import org.jetbrains.kotlinx.dataframe.api.chunked
import org.jetbrains.kotlinx.dataframe.api.forEach
import org.jetbrains.kotlinx.dataframe.api.toList
import java.nio.file.Path
import java.util.concurrent.Future
import kotlin.io.path.notExists
import kotlin.system.exitProcess

class KafkaProducerService<T> constructor(val topic: String)
    where T : KafkaSerializable {

    val logger = KotlinLogging.logger {}

    companion object {
        const val DATAFRAME_CHUNK_SIZE = 10_000
    }

    inline fun <reified T : KafkaSerializable> fromCsv(
        filepath: Path,
        csvReaderFunction: (Path, Boolean) -> DataFrame<T>
    ) {
        logger.info { "Attempting to fetch CSV file..." }
        if (filepath.notExists()) {
            logger.error { "Could not load CSV. File not found!" }
            exitProcess(-1)
        }

        logger.info { "Loading CSV to DataFrame..." }
        val dataFrame: DataFrame<T> = csvReaderFunction(filepath, true)

        logger.info { "Preparing to push messages to Kafka (topic='${topic}')" }
        val kafkaJsonProducer = KafkaJsonProducer<T>()

        dataFrame.chunked(DATAFRAME_CHUNK_SIZE).forEach { chunk ->
            val records: List<T> = chunk.toList()
            val futures: List<Future<RecordMetadata>> = kafkaJsonProducer.push(records, topic = topic)
            logger.info { "Awaiting for all messages to be successfully sent..." }
            futures.forEach { it.get() }
        }

        logger.info { "All done!" }
    }
}
