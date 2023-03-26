package club.datatalks.kafka.dto

import com.fasterxml.jackson.databind.PropertyNamingStrategies
import com.fasterxml.jackson.databind.annotation.JsonNaming


@JsonNaming(PropertyNamingStrategies.UpperSnakeCaseStrategy::class)
data class OverallPickupStatsDTO(
    val dummyCol: Int,
    val totalGreenRecords: Long,
    val totalFhvRecords: Long,
    val overallRecords: Long
)

