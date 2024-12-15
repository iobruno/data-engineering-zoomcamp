package club.datatalks.kafka.dto

import club.datatalks.kafka.infrastructure.KafkaSerializable
import com.fasterxml.jackson.annotation.JsonCreator
import com.fasterxml.jackson.annotation.JsonProperty
import com.fasterxml.jackson.databind.PropertyNamingStrategies
import com.fasterxml.jackson.databind.annotation.JsonNaming
import org.jetbrains.kotlinx.dataframe.DataFrame
import org.jetbrains.kotlinx.dataframe.api.cast
import org.jetbrains.kotlinx.dataframe.io.readCsv
import java.nio.file.Path


@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy::class)
data class FhvDTO @JsonCreator constructor(
    @JsonProperty("dispatching_base_number") val dispatchingBaseNumber: String?,
    @JsonProperty("pickup_datetime") val pickupDatetime: String,
    @JsonProperty("dropoff_datetime") val dropoffDatetime: String,
    @JsonProperty("pickup_location_id") val pickupLocationId: Int?,
    @JsonProperty("dropoff_location_id") val dropoffLocationId: Int?,
    @JsonProperty("sr_flag") val srFlag: String?,
    @JsonProperty("affiliated_base_number") val affiliatedBaseNumber: String?
) : KafkaSerializable {

    companion object {
        fun fromCsv(filepath: Path, hasHeader: Boolean = true): DataFrame<FhvDTO> {
            return DataFrame.readCsv(
                file = filepath.toFile(),
                skipLines = if (hasHeader) 1 else 0,
                header = listOf(
                    "dispatchingBaseNumber",
                    "pickupDatetime",
                    "dropoffDatetime",
                    "pickupLocationId",
                    "dropoffLocationId",
                    "srFlag",
                    "affiliatedBaseNumber",
                )
            ).cast<FhvDTO>()
        }
    }

    override fun messageKey(): String = pickupLocationId.toString()
}
