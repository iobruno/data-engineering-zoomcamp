package club.datatalks.kafka.dto

import club.datatalks.kafka.infrastructure.CsvDeserializable
import club.datatalks.kafka.infrastructure.KafkaSerializable
import com.fasterxml.jackson.databind.PropertyNamingStrategies
import com.fasterxml.jackson.databind.annotation.JsonNaming
import com.fasterxml.jackson.dataformat.csv.CsvSchema
import java.io.BufferedReader


@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy::class)
data class FhvTaxiDTO(
    val dispatchingBaseNumber: String,
    val pickupDatetime: String,
    val dropoffDatetime: String,
    val pickupLocationId: Int?,
    val dropoffLocationId: Int?,
    val srFlag: String?,
    val affiliatedBaseNumber: String
) : CsvDeserializable<FhvTaxiDTO>, KafkaSerializable {

    companion object {

        fun fromCsv(reader: BufferedReader, containsHeader: Boolean = true): Sequence<FhvTaxiDTO> =
            CsvDeserializable.seqFromCsv(reader, schema = csvSchema(), containsHeader = containsHeader)

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