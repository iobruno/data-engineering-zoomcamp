package club.datatalks.kafka.cli

import club.datatalks.kafka.dto.FhvTaxiDTO
import club.datatalks.kafka.dto.GreenTaxiDTO
import club.datatalks.kafka.dto.YellowTaxiDTO
import club.datatalks.kafka.service.KafkaJsonProducerService
import picocli.CommandLine
import picocli.CommandLine.Command
import java.nio.file.Paths


abstract class ProducerOptions {
    @CommandLine.Option(
        names = ["-i", "--csv-file"],
        required = true,
        description = ["CSV file path"]
    )
    var csvFilePath: String = ""

    @CommandLine.Option(
        names = ["-t", "--topic"],
        required = true,
        description = ["Target Kafka topic for records"]
    )
    var topic: String = ""
}

@Command(name = "green", description = ["Process GreenTaxiDTO data from CSV file and publish to Kafka topic"])
class GreenTaxiJsonProducerCommand : ProducerOptions(), Runnable {

    override fun run() {
        val greenTripDataCsvPath = Paths.get(csvFilePath)
        val greenTaxiProducer = KafkaJsonProducerService<GreenTaxiDTO>(topic)
        greenTaxiProducer.fromCsv(greenTripDataCsvPath, GreenTaxiDTO::fromCsv)
    }
}

@Command(name = "yellow", description = ["Process YellowTaxiDTO data from CSV file and publish to Kafka topic"])
class YellowTaxiJsonProducerCommand : ProducerOptions(), Runnable {

    override fun run() {
        val yellowTripDataCsvPath = Paths.get(csvFilePath)
        val yellowTaxiProducer = KafkaJsonProducerService<YellowTaxiDTO>(topic)
        yellowTaxiProducer.fromCsv(yellowTripDataCsvPath, YellowTaxiDTO::fromCsv)
    }
}

@Command(name = "fhv", description = ["Process FhvTaxiDTO data from CSV file and publish to Kafka topic"])
class FhvTaxiJsonProducerCommand :ProducerOptions(), Runnable {

    override fun run() {
        val fhvTripDataCsvPath = Paths.get(csvFilePath)
        val fhvTaxiProducer = KafkaJsonProducerService<FhvTaxiDTO>(topic)
        fhvTaxiProducer.fromCsv(fhvTripDataCsvPath, FhvTaxiDTO::fromCsv)
    }
}
