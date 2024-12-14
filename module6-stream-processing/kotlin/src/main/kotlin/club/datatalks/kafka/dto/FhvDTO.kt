package club.datatalks.kafka.dto

import club.datatalks.kafka.infrastructure.KafkaSerializable
import com.fasterxml.jackson.databind.PropertyNamingStrategies
import com.fasterxml.jackson.databind.annotation.JsonNaming
import org.jetbrains.kotlinx.dataframe.DataFrame
import org.jetbrains.kotlinx.dataframe.api.toListOf
import org.jetbrains.kotlinx.dataframe.io.readCSV
import java.nio.file.Path


@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy::class)
data class FhvDTO(
    val dispatchingBaseNumber: String,
    val pickupDatetime: String,
    val dropoffDatetime: String,
    val pickupLocationId: Int?,
    val dropoffLocationId: Int?,
    val srFlag: String?,
    val affiliatedBaseNumber: String
) : KafkaSerializable {

    companion object {
        fun fromCsv(filepath: Path, hasHeader: Boolean = true): Sequence<FhvDTO> =
            DataFrame.readCSV(
                fileOrUrl = filepath.toString(),
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
            ).toListOf<FhvDTO>().asSequence()
    }

    override fun messageKey(): String = pickupLocationId.toString()
}
