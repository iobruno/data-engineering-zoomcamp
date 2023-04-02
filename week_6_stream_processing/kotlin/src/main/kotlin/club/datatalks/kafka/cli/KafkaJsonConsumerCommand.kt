package club.datatalks.kafka.cli

import club.datatalks.kafka.service.KafkaJsonConsumerService
import club.datatalks.kafka.dto.FhvTaxiDTO
import club.datatalks.kafka.dto.GreenTaxiDTO
import club.datatalks.kafka.dto.YellowTaxiDTO
import picocli.CommandLine
import picocli.CommandLine.Command


abstract class ConsumerOptions {
    @CommandLine.Option(
        names = ["-t", "--topic"],
        required = true,
        description = ["Kafka topic where the records will be fetched from"]
    )
    var topic: String = ""

    @CommandLine.Option(
        names = ["-g", "--consumer-group"],
        required = true,
        description = ["Kafka Consumer Group"]
    )
    var consumerGroup: String = ""
}

@Command(name = "green")
class GreenTaxiJsonConsumerCommand : ConsumerOptions(), Runnable {

    override fun run() {
        val greenTaxiConsumer = KafkaJsonConsumerService(topic, consumerGroup, GreenTaxiDTO::class.java)
        greenTaxiConsumer.start()
    }
}

@Command(name = "yellow")
class YellowTaxiJsonConsumerCommand : ConsumerOptions(), Runnable {

    override fun run() {
        val yellowTaxiConsumer = KafkaJsonConsumerService(topic, consumerGroup, YellowTaxiDTO::class.java)
        yellowTaxiConsumer.start()
    }
}

@Command(name = "fhv")
class FhvTaxiJsonConsumerCommand : ConsumerOptions(), Runnable {

    override fun run() {
        val fhvTaxiConsumer = KafkaJsonConsumerService(topic, consumerGroup, FhvTaxiDTO::class.java)
        fhvTaxiConsumer.start()
    }
}
