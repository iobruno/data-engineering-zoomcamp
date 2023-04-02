package club.datatalks.kafka

import club.datatalks.kafka.cli.CLIRootCommand
import picocli.CommandLine

object CliApplication {

    @JvmStatic
    fun main(args: Array<String>) {
        CommandLine(CLIRootCommand()).execute(*args)
    }
}
