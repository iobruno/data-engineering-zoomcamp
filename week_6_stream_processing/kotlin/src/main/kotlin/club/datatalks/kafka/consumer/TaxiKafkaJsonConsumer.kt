package club.datatalks.kafka.consumer

import club.datatalks.kafka.dto.FhvTaxiDTO
import club.datatalks.kafka.dto.GreenTaxiDTO
import club.datatalks.kafka.dto.OverallPickupStatsDTO
import club.datatalks.kafka.dto.YellowTaxiDTO

class GreenTaxiKafkaJsonConsumer(
    private val kafkaTopic: String,
    private val consumerGroup: String? = null,
) : AbstractKafkaJsonConsumer<GreenTaxiDTO>(
    kafkaTopic, consumerGroup, GreenTaxiDTO::class.java
)

class YellowTaxiKafkaJsonConsumer(
    private val kafkaTopic: String,
    private val consumerGroup: String? = null,
) : AbstractKafkaJsonConsumer<YellowTaxiDTO>(
    kafkaTopic, consumerGroup, YellowTaxiDTO::class.java
)

class FhvTaxiKafkaJsonConsumer(
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
