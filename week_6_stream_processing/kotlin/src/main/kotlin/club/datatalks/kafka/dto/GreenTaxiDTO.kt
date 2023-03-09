package club.datatalks.kafka.dto

import club.datatalks.kafka.infrastructure.CsvDeserializable
import club.datatalks.kafka.infrastructure.KafkaSerializable
import com.fasterxml.jackson.databind.PropertyNamingStrategies
import com.fasterxml.jackson.databind.annotation.JsonNaming
import com.fasterxml.jackson.dataformat.csv.CsvSchema
import java.io.BufferedReader


@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy::class)
data class GreenTaxiDTO(
    val vendorId: Int,
    val pickupDatetime: String,
    val dropoffDatetime: String,
    val storeAndForward: String,
    val rateCodeId: Int,
    val pickupLocationId: Int,
    val dropoffLocationId: Int,
    val passengerCount: Int,
    val tripDistance: Double,
    val fareAmount: Double,
    val extra: Double,
    val mtaTax: Double,
    val tipAmount: Double,
    val tollsAmount: Double,
    val ehailFee: Double,
    val improvementSurcharge: Double,
    val totalAmount: Double,
    val paymentType: Int,
    val tripType: Double?,
    val congestionSurcharge: Double
) : KafkaSerializable {

    companion object {
        fun fromCsv(reader: BufferedReader, containsHeader: Boolean = true): Sequence<GreenTaxiDTO> =
            CsvDeserializable.seqFromCsv(reader, schema = csvSchema(), containsHeader = containsHeader)

        private fun csvSchema(): CsvSchema =
            CsvSchema.builder()
                .addColumn("vendor_id")
                .addColumn("pickup_datetime")
                .addColumn("dropoff_datetime")
                .addColumn("store_and_forward")
                .addColumn("rate_code_id")
                .addColumn("pickup_location_id")
                .addColumn("dropoff_location_id")
                .addColumn("passenger_count")
                .addColumn("trip_distance")
                .addColumn("fare_amount")
                .addColumn("extra")
                .addColumn("mta_tax")
                .addColumn("tip_amount")
                .addColumn("tolls_amount")
                .addColumn("ehail_fee")
                .addColumn("improvement_surcharge")
                .addColumn("total_amount")
                .addColumn("payment_type")
                .addColumn("trip_type")
                .addColumn("congestion_surcharge")
                .build()
    }

    override fun messageKey(): String = pickupLocationId.toString()

}

