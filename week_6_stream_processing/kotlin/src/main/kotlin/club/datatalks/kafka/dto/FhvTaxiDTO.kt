package club.datatalks.kafka.dto

import com.fasterxml.jackson.databind.PropertyNamingStrategies
import com.fasterxml.jackson.databind.annotation.JsonNaming
import com.fasterxml.jackson.dataformat.csv.CsvMapper
import com.fasterxml.jackson.dataformat.csv.CsvSchema
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule
import com.fasterxml.jackson.module.kotlin.KotlinModule
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
) {
    companion object {
        fun listFromCsv(reader: BufferedReader, constainsHeader: Boolean = true): List<FhvTaxiDTO> {
            val schema = if (constainsHeader)
                csvSchema().withHeader()
            else
                csvSchema().withoutHeader()

            val mapper = CsvMapper()
                .registerModule(KotlinModule.Builder().build())
                .registerModule(JavaTimeModule())

            return mapper
                .readerFor(FhvTaxiDTO::class.java)
                .with(schema)
                .readValues<FhvTaxiDTO>(reader)
                .readAll()!!
        }

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

}