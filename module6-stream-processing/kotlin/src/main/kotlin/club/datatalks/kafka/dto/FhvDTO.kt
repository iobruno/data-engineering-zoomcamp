package club.datatalks.kafka.dto

import club.datatalks.kafka.infrastructure.CsvDeserializable
import club.datatalks.kafka.infrastructure.KafkaSerializable
import com.fasterxml.jackson.annotation.JsonCreator
import com.fasterxml.jackson.annotation.JsonProperty
import com.fasterxml.jackson.databind.PropertyNamingStrategies
import com.fasterxml.jackson.databind.annotation.JsonNaming
import com.fasterxml.jackson.dataformat.csv.CsvSchema
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

        /**
         * create() is meant for each row from the CsvFile into an FhvTaxiDTO object
         * using the Jackson's @JsonCreator
         */
        @JvmStatic
        @JsonCreator
        fun create(
            @JsonProperty("dispatching_base_number") dispatchingBaseNumber: String,
            @JsonProperty("pickup_datetime") pickupDatetime: String,
            @JsonProperty("dropoff_datetime") dropoffDatetime: String,
            @JsonProperty("pickup_location_id") pickupLocationId: Int?,
            @JsonProperty("dropoff_location_id") dropoffLocationId: Int?,
            @JsonProperty("sr_flag") srFlag: String?,
            @JsonProperty("affiliated_base_number") affiliatedBaseNumber: String
        ) = FhvDTO(
            dispatchingBaseNumber, pickupDatetime, dropoffDatetime, pickupLocationId,
            dropoffLocationId, srFlag, affiliatedBaseNumber
        )

        fun fromCsv(filepath: Path, containsHeader: Boolean = true): Sequence<FhvDTO> =
            CsvDeserializable.seqFromCsv(filepath, schema = csvSchema(), containsHeader = containsHeader)

        private fun csvSchema(): CsvSchema =
            CsvSchema.builder()
                .addColumn("dispatching_base_number")
                .addColumn("pickup_datetime")
                .addColumn("dropoff_datetime")
                .addColumn("pickup_location_id")
                .addColumn("dropoff_location_id")
                .addColumn("sr_flag")
                .addColumn("affiliated_base_number")
                .build()
    }

    override fun messageKey(): String = pickupLocationId.toString()

}
