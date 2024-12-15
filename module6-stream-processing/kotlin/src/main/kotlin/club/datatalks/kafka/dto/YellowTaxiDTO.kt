package club.datatalks.kafka.dto

import club.datatalks.kafka.infrastructure.KafkaSerializable
import com.fasterxml.jackson.databind.PropertyNamingStrategies
import com.fasterxml.jackson.databind.annotation.JsonNaming
import org.jetbrains.kotlinx.dataframe.DataFrame
import org.jetbrains.kotlinx.dataframe.api.cast
import org.jetbrains.kotlinx.dataframe.io.readCsv
import java.nio.file.Path


@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy::class)
data class YellowTaxiDTO(
    val vendorId: Int,
    val pickupDatetime: String,
    val dropoffDatetime: String,
    val passengerCount: Int,
    val tripDistance: Double,
    val rateCodeId: Int,
    val storeAndForward: String,
    val pickupLocationId: Int,
    val dropoffLocationId: Int,
    val paymentType: Int,
    val fareAmount: Double,
    val extra: Double,
    val mtaTax: Double,
    val tipAmount: Double,
    val tollsAMount: Double,
    val improvementSurcharge: Double,
    val totalAmount: Double,
    val congestionSurcharge: Double?
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
