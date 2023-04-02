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
        description = ["Source Kafka topic for records"]
    )
    var topic: String = ""

    @CommandLine.Option(
        names = ["-g", "--consumer-group"],
        required = true,
        description = ["Consumer group to subscribe to the Source kafka topic"]
    )
    var consumerGroup: String = ""
}

@Command(name = "green", description = ["Deserialize ConsumerRecords from source Kafka topic to GreenTaxiDTO"])
class GreenTaxiJsonConsumerCommand : ConsumerOptions(), Runnable {

    override fun run() {
        val greenTaxiConsumer = KafkaJsonConsumerService(topic, consumerGroup, GreenTaxiDTO::class.java)
        greenTaxiConsumer.start()
    }
}

@Command(name = "yellow", description = ["Deserialize ConsumerRecords from source Kafka topic to YellowTaxiDTO"])
class YellowTaxiJsonConsumerCommand : ConsumerOptions(), Runnable {

    override fun run() {
        val yellowTaxiConsumer = KafkaJsonConsumerService(topic, consumerGroup, YellowTaxiDTO::class.java)
        yellowTaxiConsumer.start()
    }
}

@Command(name = "fhv", description = ["Deserialize ConsumerRecords from source Kafka topic to FhvTaxiDTO"])
class FhvTaxiJsonConsumerCommand : ConsumerOptions(), Runnable {

    override fun run() {
        val fhvTaxiConsumer = KafkaJsonConsumerService(topic, consumerGroup, FhvTaxiDTO::class.java)
        fhvTaxiConsumer.start()
    }
}
