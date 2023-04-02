package club.datatalks.kafka

import club.datatalks.kafka.dto.FhvTaxiDTO
import club.datatalks.kafka.dto.GreenTaxiDTO
import club.datatalks.kafka.dto.YellowTaxiDTO
import java.nio.file.Paths


class GreenTaxiProducer(private val topic: String) :
    AbstractKafkaJsonProducer<GreenTaxiDTO>(topic)

class YellowTaxiProducer(private val topic: String) :
    AbstractKafkaJsonProducer<YellowTaxiDTO>(topic)

class FhvTaxiProducer(private val topic: String) :
    AbstractKafkaJsonProducer<FhvTaxiDTO>(topic)


fun main() {
    /** Green Taxi Producer **/
    val greenTripDataCsvPath = Paths.get("src/main/resources/green_tripdata_2019-01.csv")
    val greenTaxiProducer = GreenTaxiProducer(topic = "green_tripdata")
    greenTaxiProducer.fromCsv(greenTripDataCsvPath, GreenTaxiDTO::fromCsv)

    /** Yellow Taxi Producer **/
//    val yellowTripDataCsvPath = Paths.get("src/main/resources/yellow_tripdata_2019-01.csv")
//    val yellowTaxiProducer = YellowTaxiProducer(topic = "yellow_tripdata")
//    yellowTaxiProducer.fromCsv(yellowTripDataCsvPath, YellowTaxiDTO::fromCsv)

    /** Fhv Taxi Producer **/
//    val fhvTripDataCsvPath = Paths.get("src/main/resources/fhv_tripdata_2019-01.csv")
//    val fhvTaxiProducer = FhvTaxiProducer(topic = "fhv_tripdata")
//    fhvTaxiProducer.fromCsv(fhvTripDataCsvPath, FhvTaxiDTO::fromCsv)
}
