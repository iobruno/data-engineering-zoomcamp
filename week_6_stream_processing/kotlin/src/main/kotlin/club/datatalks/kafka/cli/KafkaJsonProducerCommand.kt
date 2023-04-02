package club.datatalks.kafka.cli

import club.datatalks.kafka.producer.FhvTaxiKafkaJsonProducer
import club.datatalks.kafka.producer.GreenTaxiKafkaJsonProducer
import club.datatalks.kafka.producer.YellowTaxiKafkaJsonProducer
import club.datatalks.kafka.dto.FhvTaxiDTO
import club.datatalks.kafka.dto.GreenTaxiDTO
import club.datatalks.kafka.dto.YellowTaxiDTO
import picocli.CommandLine
import picocli.CommandLine.Command
import java.nio.file.Paths


abstract class ProducerOptions {
    @CommandLine.Option(
        names = ["-i", "--csv-file"],
        required = true,
        description = ["Path to the .csv file"]
    )
    var csvFilePath: String = ""

    @CommandLine.Option(
        names = ["-t", "--topic"],
        required = true,
        description = ["Kafka topic where the records will be sent to"]
    )
    var topic: String = ""
}

@Command(name = "green")
class GreenTaxiJsonProducerCommand : ProducerOptions(), Runnable {

    override fun run() {
        val greenTripDataCsvPath = Paths.get(csvFilePath)
        val greenTaxiProducer = GreenTaxiKafkaJsonProducer(topic)
        greenTaxiProducer.fromCsv(greenTripDataCsvPath, GreenTaxiDTO::fromCsv)
    }
}

@Command(name = "yellow")
class YellowTaxiJsonProducerCommand : ProducerOptions(), Runnable {

    override fun run() {
        val yellowTripDataCsvPath = Paths.get(csvFilePath)
        val yellowTaxiProducer = YellowTaxiKafkaJsonProducer(topic)
        yellowTaxiProducer.fromCsv(yellowTripDataCsvPath, YellowTaxiDTO::fromCsv)
    }
}

@Command(name = "fhv")
class FhvTaxiJsonProducerCommand :ProducerOptions(), Runnable {

    override fun run() {
        val fhvTripDataCsvPath = Paths.get(csvFilePath)
        val fhvTaxiProducer = FhvTaxiKafkaJsonProducer(topic)
        fhvTaxiProducer.fromCsv(fhvTripDataCsvPath, FhvTaxiDTO::fromCsv)
    }
}
