package club.datatalks.kafka.dto

import club.datatalks.kafka.infrastructure.CsvDeserializable
import club.datatalks.kafka.infrastructure.KafkaSerializable
import com.fasterxml.jackson.annotation.JsonCreator
import com.fasterxml.jackson.annotation.JsonProperty
import com.fasterxml.jackson.databind.PropertyNamingStrategies
import com.fasterxml.jackson.databind.annotation.JsonNaming
import com.fasterxml.jackson.dataformat.csv.CsvSchema
import java.io.BufferedReader


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
    val congestionSurcharge: Double
) : KafkaSerializable {

    companion object {

        /**
         * create() is meant for each row from the CsvFile into an YellowTaxiDTO object
         * using the Jackson's @JsonCreator
         */
        @JvmStatic
        @JsonCreator
        fun create(
            @JsonProperty("vendor_id") vendorId: Int,
            @JsonProperty("pickup_datetime")  pickupDatetime: String,
            @JsonProperty("dropoff_datetime") dropoffDatetime: String,
            @JsonProperty("passenger_count") passengerCount: Int,
            @JsonProperty("trip_distance") tripDistance: Double,
            @JsonProperty("rate_code_id") rateCodeId: Int,
            @JsonProperty("store_and_forward") storeAndForward: String,
            @JsonProperty("pickup_location_id") pickupLocationId: Int,
            @JsonProperty("dropoff_location_id") dropoffLocationId: Int,
            @JsonProperty("payment_type") paymentType: Int,
            @JsonProperty("fare_amount") fareAmount: Double,
            @JsonProperty("extra") extra: Double,
            @JsonProperty("mta_tax") mtaTax: Double,
            @JsonProperty("tip_amount") tipAmount: Double,
            @JsonProperty("tolls_amount") tollsAMount: Double,
            @JsonProperty("improvement_surcharge") improvementSurcharge: Double,
            @JsonProperty("total_amount") totalAmount: Double,
            @JsonProperty("congestion_surcharge") congestionSurcharge: Double
        ) = YellowTaxiDTO(
            vendorId, pickupDatetime, dropoffDatetime, passengerCount, tripDistance, rateCodeId, storeAndForward,
            pickupLocationId, dropoffLocationId, paymentType, fareAmount, extra, mtaTax, tipAmount, tollsAMount,
            improvementSurcharge, totalAmount, congestionSurcharge
        )

        fun fromCsv(reader: BufferedReader, containsHeader: Boolean = true): Sequence<YellowTaxiDTO> =
            CsvDeserializable.seqFromCsv(reader, schema = csvSchema(), containsHeader = containsHeader)

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

    override fun messageKey(): String = pickupLocationId.toString()

}
