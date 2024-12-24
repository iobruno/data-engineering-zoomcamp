package club.datatalks.kafka.cli

import club.datatalks.kafka.dto.FhvDTO
import club.datatalks.kafka.dto.GreenTaxiDTO
import club.datatalks.kafka.dto.YellowTaxiDTO
import club.datatalks.kafka.service.KafkaConsumerService
import picocli.CommandLine.Command
import picocli.CommandLine.Option


abstract class ConsumerOptions {
    @Option(names = ["-t", "--topic"], required = true, description = ["Kafka topic to subscribe to"])
    lateinit var topic: String

    @Option(names = ["-g", "--consumer-group"], required = true, description = ["Kafka consumer group name"])
    lateinit var consumerGroup: String
}

@Command(name = "green", description = ["Deserialize ConsumerRecords from source Kafka topic to GreenTaxiDTO"])
class GreenTaxiJsonConsumerCommand : ConsumerOptions(), Runnable {

    override fun run() {
        val consumer = KafkaConsumerService(topic, consumerGroup, GreenTaxiDTO::class)
        consumer.start()
    }
}

@Command(name = "yellow", description = ["Deserialize ConsumerRecords from source Kafka topic to YellowTaxiDTO"])
class YellowTaxiJsonConsumerCommand : ConsumerOptions(), Runnable {

    override fun run() {
        val consumer = KafkaConsumerService(topic, consumerGroup, YellowTaxiDTO::class)
        consumer.start()
    }
}

@Command(name = "fhv", description = ["Deserialize ConsumerRecords from source Kafka topic to FhvTaxiDTO"])
class FhvTaxiJsonConsumerCommand : ConsumerOptions(), Runnable {

    override fun run() {
        val consumer = KafkaConsumerService(topic, consumerGroup, FhvDTO::class)
        consumer.start()
    }
}
