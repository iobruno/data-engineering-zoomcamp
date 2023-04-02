package club.datatalks.kafka

import club.datatalks.kafka.dto.FhvTaxiDTO
import club.datatalks.kafka.dto.GreenTaxiDTO
import club.datatalks.kafka.dto.OverallPickupStatsDTO
import club.datatalks.kafka.dto.YellowTaxiDTO

class GreenTaxiConsumer(
    private val kafkaTopic: String,
    private val consumerGroup: String? = null,
) : AbstractKafkaJsonConsumer<GreenTaxiDTO>(
    kafkaTopic, consumerGroup, GreenTaxiDTO::class.java
)

class YellowTaxiConsumer(
    private val kafkaTopic: String,
    private val consumerGroup: String? = null,
) : AbstractKafkaJsonConsumer<YellowTaxiDTO>(
    kafkaTopic, consumerGroup, YellowTaxiDTO::class.java
)

class FhvTaxiConsumer(
    private val kafkaTopic: String,
    private val consumerGroup: String? = null,
) : AbstractKafkaJsonConsumer<FhvTaxiDTO>(
    kafkaTopic, consumerGroup, FhvTaxiDTO::class.java
)

class OverallPickupStatsConsumer(
    private val kafkaTopic: String,
    private val consumerGroup: String? = null,
) : AbstractKafkaJsonConsumer<OverallPickupStatsDTO>(
    kafkaTopic, consumerGroup, OverallPickupStatsDTO::class.java
)


fun main() {
    /** Green Taxi Consumer **/
    val greenTaxiConsumer = GreenTaxiConsumer(
        kafkaTopic = "green_tripdata",
        consumerGroup = "default"
    )
    greenTaxiConsumer.start()

    /** Yellow Taxi Producer **/
//    val yellowTaxiConsumer = YellowTaxiConsumer(
//        kafkaTopic = "yellow_tripdata",
//        consumerGroup = "default"
//    )
//    yellowTaxiConsumer.start()

    /** Fhv Taxi Producer **/
//    val fhvTaxiConsumer = FhvTaxiConsumer(
//        kafkaTopic = "fhv_tripdata",
//        consumerGroup = "default"
//    )
//    fhvTaxiConsumer.start()

    /** Overall Pickup Aggregation Stats Consumer **/
//    val overallPickupAggConsumer = OverallPickupStatsConsumer(
//        kafkaTopic = "overall_pickup_agg",
//        consumerGroup = "default"
//    )
//    overallPickupAggConsumer.start()
}
