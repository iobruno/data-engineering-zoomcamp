package club.datatalks.kafka

import club.datatalks.kafka.dto.RideDTO
import club.datatalks.kafka.infrastructure.KafkaJsonConsumer
import club.datatalks.kafka.infrastructure.KafkaJsonProducer
import mu.KotlinLogging
import org.apache.kafka.clients.consumer.ConsumerRecords
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.time.Duration
import kotlin.io.path.notExists
import kotlin.system.exitProcess


val logger = KotlinLogging.logger {}

fun runKafkaProducer(topic: String) {
    logger.info { "Attempting to fetch CSV file..." }
    val csvFilePath: Path = Paths.get("src/main/resources/rides.csv")

    if (csvFilePath.notExists()) {
        logger.error { "Could not load 'rides.csv'. File not found!" }
        exitProcess(-1)
    }

    logger.info { "Deserializing CSV into a Data Class..." }
    val reader = Files.newBufferedReader(csvFilePath)!!
    val rides = RideDTO.listFromCsv(reader)

    logger.info { "Preparing to push messages to Kafka (topic='${topic}')" }
    val kafkaJsonProducer = KafkaJsonProducer<RideDTO>()
    kafkaJsonProducer.push(rides, topic = topic)

    logger.info { "All done!" }
}

fun runKafkaConsumer(kafkaTopic: String) {
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


fun main() {
    val kafkaTopic = "rides"
//    runKafkaProducer(kafkaTopic)
    runKafkaConsumer(kafkaTopic)
}
