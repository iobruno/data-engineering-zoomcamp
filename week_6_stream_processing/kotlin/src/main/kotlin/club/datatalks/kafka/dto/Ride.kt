package club.datatalks.kafka.dto

import com.fasterxml.jackson.dataformat.csv.CsvMapper
import com.fasterxml.jackson.dataformat.csv.CsvSchema
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule
import com.fasterxml.jackson.module.kotlin.KotlinModule
import java.io.BufferedReader

data class Ride(
    val vendorId: Int,
    val pickupDateTime: String,
    val dropOffDateTime: String,
    val passengerCount: Int,
    val tripDistance: Double,
    val rateCodeId: Int,
    val storeAndForward: String,
    val pickupLocationId: Int,
    val dropOffLocationId: Int,
    val paymentType: Int,
    val fareAmount: Double,
    val extra: Double,
    val mtaTax: Double,
    val tipAmount: Double,
    val tollsAMount: Double,
    val improvementSurcharge: Double,
    val totalAmount: Double,
    val congestionSurcharge: Double
) {

    companion object {
        fun listFromCsv(reader: BufferedReader, containsHeader: Boolean = true): List<Ride> {
            val schema = if (containsHeader)
                csvSchema().withHeader()
            else
                csvSchema().withoutHeader()

            val mapper = CsvMapper()
                .registerModule(KotlinModule.Builder().build())
                .registerModule(JavaTimeModule())

            return mapper
                .readerFor(Ride::class.java)
                .with(schema)
                .readValues<Ride>(reader)
                .readAll()!!
        }

        private fun csvSchema(): CsvSchema = CsvSchema.builder()
            .addColumn(Ride::vendorId.name)
            .addColumn(Ride::pickupDateTime.name)
            .addColumn(Ride::dropOffDateTime.name)
            .addColumn(Ride::passengerCount.name)
            .addColumn(Ride::tripDistance.name)
            .addColumn(Ride::rateCodeId.name)
            .addColumn(Ride::storeAndForward.name)
            .addColumn(Ride::pickupLocationId.name)
            .addColumn(Ride::dropOffLocationId.name)
            .addColumn(Ride::paymentType.name)
            .addColumn(Ride::fareAmount.name)
            .addColumn(Ride::extra.name)
            .addColumn(Ride::mtaTax.name)
            .addColumn(Ride::tipAmount.name)
            .addColumn(Ride::tollsAMount.name)
            .addColumn(Ride::improvementSurcharge.name)
            .addColumn(Ride::totalAmount.name)
            .addColumn(Ride::congestionSurcharge.name)
            .build()
    }
}
