package club.datatalks.kafka.dto

import club.datatalks.kafka.infrastructure.KafkaSerializable
import com.fasterxml.jackson.databind.PropertyNamingStrategies
import com.fasterxml.jackson.databind.annotation.JsonNaming
import org.jetbrains.kotlinx.dataframe.DataFrame
import org.jetbrains.kotlinx.dataframe.api.cast
import org.jetbrains.kotlinx.dataframe.io.readCsv
import java.nio.file.Path


@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy::class)
data class GreenTaxiDTO(
    val vendorId: Int,
    val pickupDatetime: String,
    val dropoffDatetime: String,
    val storeAndForward: String,
    val rateCodeId: Int,
    val pickupLocationId: Int,
    val dropOffLocationId: Int,
    val passengerCount: Int,
    val tripDistance: Double,
    val fareAmount: Double,
    val extra: Double,
    val mtaTax: Double,
    val tipAmount: Double,
    val tollsAmount: Double,
    val ehailFee: Double?,
    val improvementSurcharge: Double,
    val totalAmount: Double,
    val paymentType: Int,
    val tripType: Double?,
    val congestionSurcharge: Double?
) : KafkaSerializable {

    companion object {
        fun fromCsv(filepath: Path, hasHeader: Boolean = true): DataFrame<GreenTaxiDTO> =
            DataFrame.readCsv(
                file = filepath.toFile(),
                skipLines = if (hasHeader) 1 else 0,
                header = listOf(
                    "vendorId",
                    "pickupDatetime",
                    "dropoffDatetime",
                    "storeAndForward",
                    "rateCodeId",
                    "pickupLocationId",
                    "dropOffLocationId",
                    "passengerCount",
                    "tripDistance",
                    "fareAmount",
                    "extra",
                    "mtaTax",
                    "tipAmount",
                    "tollsAmount",
                    "ehailFee",
                    "improvementSurcharge",
                    "totalAmount",
                    "paymentType",
                    "tripType",
                    "congestionSurcharge",
                )
            ).cast<GreenTaxiDTO>()
    }

    override fun messageKey(): String = pickupLocationId.toString()
}
