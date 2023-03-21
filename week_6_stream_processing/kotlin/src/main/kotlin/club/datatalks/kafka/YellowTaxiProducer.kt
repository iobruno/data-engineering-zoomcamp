package club.datatalks.kafka

import club.datatalks.kafka.dto.YellowTaxiDTO
import club.datatalks.kafka.infrastructure.KafkaJsonProducer
import mu.KotlinLogging
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import kotlin.io.path.notExists
import kotlin.system.exitProcess


val logger = KotlinLogging.logger {}

fun main() {
    val topic = "yellow_taxi_rides"

    logger.info { "Attempting to fetch CSV file..." }
    val csvFilePath: Path = Paths.get("src/main/resources/yellow_tripdata_2019-01.csv")

    if (csvFilePath.notExists()) {
        logger.error { "Could not load 'yellow_tripdata_2019-01.csv'. File not found!" }
        exitProcess(-1)
    }

    logger.info { "Deserializing CSV into a Data Class..." }
    val reader = Files.newBufferedReader(csvFilePath)!!
    val rides: List<YellowTaxiDTO> = YellowTaxiDTO.listFromCsv(reader)

    logger.info { "Preparing to push messages to Kafka (topic='${topic}')" }
    val kafkaJsonProducer = KafkaJsonProducer<YellowTaxiDTO>()
    val futures = kafkaJsonProducer.push(rides, topic = topic)

    logger.info { "Awaiting for all messages to be successfully sent..." }
    futures.forEach { it.get() }

    logger.info { "All done!" }
}
