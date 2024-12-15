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
data class YellowTaxiDTO @JsonCreator constructor(
    @JsonProperty("vendor_id") val vendorId: Int,
    @JsonProperty("pickup_datetime") val pickupDatetime: String,
    @JsonProperty("dropoff_datetime") val dropoffDatetime: String,
    @JsonProperty("passenger_count") val passengerCount: Int,
    @JsonProperty("trip_distance") val tripDistance: Double,
    @JsonProperty("rate_code_id") val rateCodeId: Int,
    @JsonProperty("store_and_forward") val storeAndForward: String,
    @JsonProperty("pickup_location_id") val pickupLocationId: Int,
    @JsonProperty("dropoff_location_id") val dropoffLocationId: Int,
    @JsonProperty("payment_type") val paymentType: Int,
    @JsonProperty("fare_amount") val fareAmount: Double,
    @JsonProperty("extra") val extra: Double,
    @JsonProperty("mta_tax") val mtaTax: Double,
    @JsonProperty("tip_amount") val tipAmount: Double,
    @JsonProperty("tolls_amount") val tollsAMount: Double,
    @JsonProperty("improvement_surcharge") val improvementSurcharge: Double,
    @JsonProperty("total_amount") val totalAmount: Double,
    @JsonProperty("congestion_surcharge") val congestionSurcharge: Double?
) : KafkaSerializable {

    companion object {
        fun fromCsv(filepath: Path, hasHeader: Boolean = true): DataFrame<YellowTaxiDTO> =
            DataFrame.readCsv(
                file = filepath.toFile(),
                skipLines = if (hasHeader) 1 else 0,
                header = listOf(
                    "vendorId",
                    "pickupDatetime",
                    "dropoffDatetime",
                    "passengerCount",
                    "tripDistance",
                    "rateCodeId",
                    "storeAndForward",
                    "pickupLocationId",
                    "dropoffLocationId",
                    "paymentType",
                    "fareAmount",
                    "extra",
                    "mtaTax",
                    "tipAmount",
                    "tollsAMount",
                    "improvementSurcharge",
                    "totalAmount",
                    "congestionSurcharge",
                )
            ).cast<YellowTaxiDTO>()
    }

    override fun messageKey(): String = pickupLocationId.toString()
}
