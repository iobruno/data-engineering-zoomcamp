package club.datatalks.kafka.dto

import club.datatalks.kafka.infrastructure.KafkaSerializable
import com.fasterxml.jackson.annotation.JsonProperty
import com.fasterxml.jackson.databind.PropertyNamingStrategies
import com.fasterxml.jackson.databind.PropertyNamingStrategy
import com.fasterxml.jackson.databind.annotation.JsonNaming
import com.fasterxml.jackson.dataformat.csv.CsvMapper
import com.fasterxml.jackson.dataformat.csv.CsvSchema
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule
import com.fasterxml.jackson.module.kotlin.KotlinModule
import java.io.BufferedReader

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy::class)
data class RideDTO(
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
    val congestionSurcharge: Double
) : KafkaSerializable {

    companion object {
        fun listFromCsv(reader: BufferedReader, containsHeader: Boolean = true): List<RideDTO> {
            val schema = if (containsHeader)
                csvSchema().withHeader()
            else
                csvSchema().withoutHeader()

            val mapper = CsvMapper()
                .registerModule(KotlinModule.Builder().build())
                .registerModule(JavaTimeModule())

            return mapper
                .readerFor(RideDTO::class.java)
                .with(schema)
                .readValues<RideDTO>(reader)
                .readAll()!!
        }

        private fun csvSchema(): CsvSchema =
            CsvSchema.builder()
                .addColumn("vendor_id")
                .addColumn("pickup_datetime")
                .addColumn("dropoff_datetime")
                .addColumn("passenger_count")
                .addColumn("trip_distance")
                .addColumn("rate_code_id")
                .addColumn("store_and_forward")
                .addColumn("pickup_location_id")
                .addColumn("dropoff_location_id")
                .addColumn("payment_type")
                .addColumn("fare_amount")
                .addColumn("extra")
                .addColumn("mta_tax")
                .addColumn("tip_amount")
                .addColumn("tolls_amount")
                .addColumn("improvement_surcharge")
                .addColumn("total_amount")
                .addColumn("congestion_surcharge")
                .build()
    }

    override fun messageKey(): String =
        pickupLocationId.toString()

}
