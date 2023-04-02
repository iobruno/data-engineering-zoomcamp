package club.datatalks.kafka.cli

import picocli.CommandLine.Command
import picocli.CommandLine.HelpCommand


@Command(subcommands = [
    HelpCommand::class,
    KafkaJsonProducerRootCommand::class,
    KafkaJsonConsumerRootCommand::class
])
class CLIRootCommand


@Command(name = "producer", subcommands = [
    GreenTaxiJsonProducerCommand::class,
    YellowTaxiJsonProducerCommand::class,
    FhvTaxiJsonProducerCommand::class
])
class KafkaJsonProducerRootCommand


@Command(name = "consumer", subcommands = [
    GreenTaxiJsonConsumerCommand::class,
    YellowTaxiJsonConsumerCommand::class,
    FhvTaxiJsonConsumerCommand::class
])
class KafkaJsonConsumerRootCommand
