package club.datatalks.kafka.cli

import club.datatalks.kafka.consumer.FhvTaxiKafkaJsonConsumer
import club.datatalks.kafka.consumer.GreenTaxiKafkaJsonConsumer
import club.datatalks.kafka.consumer.YellowTaxiKafkaJsonConsumer
import picocli.CommandLine
import picocli.CommandLine.Command


open class ConsumerOptions {
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
        val greenTaxiConsumer = GreenTaxiKafkaJsonConsumer(topic, consumerGroup)
        greenTaxiConsumer.start()
    }
}

@Command(name = "yellow")
class YellowTaxiJsonConsumerCommand : ConsumerOptions(), Runnable {

    override fun run() {
        val yellowTaxiConsumer = YellowTaxiKafkaJsonConsumer(topic, consumerGroup)
        yellowTaxiConsumer.start()
    }
}

@Command(name = "fhv")
class FhvTaxiJsonConsumerCommand : ConsumerOptions(), Runnable {

    override fun run() {
        val fhvTaxiConsumer = FhvTaxiKafkaJsonConsumer(topic, consumerGroup)
        fhvTaxiConsumer.start()
    }
}
