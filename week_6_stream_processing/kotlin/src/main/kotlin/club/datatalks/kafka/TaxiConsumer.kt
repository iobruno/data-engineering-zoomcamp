package club.datatalks.kafka

import club.datatalks.kafka.dto.FhvTaxiDTO
import club.datatalks.kafka.dto.GreenTaxiDTO
import club.datatalks.kafka.dto.OverallPickupStatsDTO

class GreenTaxiConsumer(
    private val kafkaTopic: String,
    private val consumerGroup: String? = null,
) : AbstractKafkaJsonConsumer(kafkaTopic, consumerGroup, GreenTaxiDTO::class.java)


class YellowTaxiConsumer(
    private val kafkaTopic: String,
    private val consumerGroup: String? = null,
) : AbstractKafkaJsonConsumer(kafkaTopic, consumerGroup, YellowTaxiConsumer::class.java)


class FhvTaxiConsumer(
    private val kafkaTopic: String,
    private val consumerGroup: String? = null,
) : AbstractKafkaJsonConsumer(kafkaTopic, consumerGroup, FhvTaxiDTO::class.java)


class OverallPickupStatsConsumer(
    private val kafkaTopic: String,
    private val consumerGroup: String? = null,
) : AbstractKafkaJsonConsumer(kafkaTopic, consumerGroup, OverallPickupStatsDTO::class.java)


fun main() {
    val greenTaxiConsumer = GreenTaxiConsumer(
        kafkaTopic = "green_tripdata",
        consumerGroup = "default"
    )
    val yellowTaxiConsumer = YellowTaxiConsumer(
        kafkaTopic = "yellow_tripdata",
        consumerGroup = "default"
    )
    val fhvTaxiConsumer = FhvTaxiConsumer(
        kafkaTopic = "green_tripdata",
        consumerGroup = "default"
    )
    val overall_pickup_agg = OverallPickupStatsConsumer(
        kafkaTopic = "overall_pickup_agg",
        consumerGroup = "default"
    )

    greenTaxiConsumer.start()
}
