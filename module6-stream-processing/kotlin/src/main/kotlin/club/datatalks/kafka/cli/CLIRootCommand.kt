package club.datatalks.kafka.cli

import picocli.CommandLine.Command
import picocli.CommandLine.HelpCommand


@Command(subcommands = [
    HelpCommand::class,
    KafkaJsonProducerRootCommand::class,
    KafkaJsonConsumerRootCommand::class
])
open class CLIRootCommand()


@Command(
    name = "producer",
    description = ["Parse data from source dataset and publish as JSON to Kafka"],
    subcommands = [
        GreenTaxiJsonProducerCommand::class,
        YellowTaxiJsonProducerCommand::class,
        FhvTaxiJsonProducerCommand::class
    ]
)
open class KafkaJsonProducerRootCommand()


@Command(
    name = "consumer",
    description = ["Subscribe and consume records from Kafka topic"],
    subcommands = [
        GreenTaxiJsonConsumerCommand::class,
        YellowTaxiJsonConsumerCommand::class,
        FhvTaxiJsonConsumerCommand::class
    ]
)
open class KafkaJsonConsumerRootCommand()
