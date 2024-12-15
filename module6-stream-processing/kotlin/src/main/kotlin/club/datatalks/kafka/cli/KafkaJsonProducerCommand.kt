package club.datatalks.kafka.cli

import club.datatalks.kafka.dto.FhvDTO
import club.datatalks.kafka.dto.GreenTaxiDTO
import club.datatalks.kafka.dto.YellowTaxiDTO
import club.datatalks.kafka.service.KafkaProducerService
import picocli.CommandLine.Command
import picocli.CommandLine.Option
import java.nio.file.Paths


abstract class ProducerOptions {
    @Option(names = ["-i", "--csv-file"], required = true, description = ["CSV file path"])
    lateinit var csvFilePath: String

    @Option(names = ["-t", "--topic"], required = true, description = ["Target Kafka topic for records"])
    lateinit var topic: String
}

@Command(name = "green", description = ["Process GreenTaxiDTO data from CSV file and publish to Kafka topic"])
class GreenTaxiJsonProducerCommand : ProducerOptions(), Runnable {

    override fun run() {
        val filepath = Paths.get(csvFilePath)
        val producer = KafkaProducerService<GreenTaxiDTO>(topic)
        producer.fromCsv(filepath, GreenTaxiDTO::fromCsv)
    }
}

@Command(name = "yellow", description = ["Process YellowTaxiDTO data from CSV file and publish to Kafka topic"])
class YellowTaxiJsonProducerCommand : ProducerOptions(), Runnable {

    override fun run() {
        val filepath = Paths.get(csvFilePath)
        val producer = KafkaProducerService<YellowTaxiDTO>(topic)
        producer.fromCsv(filepath, YellowTaxiDTO::fromCsv)
    }
}

@Command(name = "fhv", description = ["Process FhvTaxiDTO data from CSV file and publish to Kafka topic"])
class FhvTaxiJsonProducerCommand : ProducerOptions(), Runnable {

    override fun run() {
        val filepath = Paths.get(csvFilePath)
        val producer = KafkaProducerService<FhvDTO>(topic)
        producer.fromCsv(filepath, FhvDTO::fromCsv)
    }
}
