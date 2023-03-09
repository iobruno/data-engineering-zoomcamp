package club.datatalks.kafka

import club.datatalks.kafka.dto.Ride
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths

fun main(args: Array<String>) {
    val csvFilePath: Path = Paths.get("src/main/resources/rides.csv")
    val reader = Files.newBufferedReader(csvFilePath)!!

    val rides = Ride.listFromCsv(reader)
    println(rides)
}
