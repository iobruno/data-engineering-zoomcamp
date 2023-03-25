package club.datatalks.kafka

import club.datatalks.kafka.dto.FhvTaxiDTO
import club.datatalks.kafka.infrastructure.KafkaJsonProducer
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import kotlin.io.path.notExists
import kotlin.system.exitProcess


fun main() {
    val topic = "fhv_tripdata"

    logger.info { "Attempting to fetch CSV file..." }
        val csvFilePath: Path = Paths.get("src/main/resources/fhv_tripdata_2019-01.csv")

    if (csvFilePath.notExists()) {
        logger.error { "Could not load 'fhv_tripdata_2019-01.csv'. File not found!" }
        exitProcess(-1)
    }

    logger.info { "Deserializing CSV into a Data Class..." }
    val reader = Files.newBufferedReader(csvFilePath)!!
    val rides: Sequence<FhvTaxiDTO> = FhvTaxiDTO.fromCsv(reader)

    logger.info { "Preparing to push messages to Kafka (topic='${topic}')" }
    val kafkaJsonProducer = KafkaJsonProducer<FhvTaxiDTO>()
    val futures = kafkaJsonProducer.push(rides, topic = topic)

    logger.info { "Awaiting for all messages to be successfully sent..." }
    futures.forEach { it.get() }

    logger.info { "All done!" }
}
