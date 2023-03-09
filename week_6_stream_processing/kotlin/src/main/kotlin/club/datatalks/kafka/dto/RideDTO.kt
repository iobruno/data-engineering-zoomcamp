package club.datatalks.kafka.dto

import club.datatalks.kafka.infrastructure.KafkaSerializable
import com.fasterxml.jackson.dataformat.csv.CsvMapper
import com.fasterxml.jackson.dataformat.csv.CsvSchema
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule
import com.fasterxml.jackson.module.kotlin.KotlinModule
import java.io.BufferedReader

data class RideDTO(
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

        private fun csvSchema(): CsvSchema = CsvSchema.builder()
            .addColumn(RideDTO::vendorId.name)
            .addColumn(RideDTO::pickupDateTime.name)
            .addColumn(RideDTO::dropOffDateTime.name)
            .addColumn(RideDTO::passengerCount.name)
            .addColumn(RideDTO::tripDistance.name)
            .addColumn(RideDTO::rateCodeId.name)
            .addColumn(RideDTO::storeAndForward.name)
            .addColumn(RideDTO::pickupLocationId.name)
            .addColumn(RideDTO::dropOffLocationId.name)
            .addColumn(RideDTO::paymentType.name)
            .addColumn(RideDTO::fareAmount.name)
            .addColumn(RideDTO::extra.name)
            .addColumn(RideDTO::mtaTax.name)
            .addColumn(RideDTO::tipAmount.name)
            .addColumn(RideDTO::tollsAMount.name)
            .addColumn(RideDTO::improvementSurcharge.name)
            .addColumn(RideDTO::totalAmount.name)
            .addColumn(RideDTO::congestionSurcharge.name)
            .build()
    }

    override fun messageKey(): String = pickupLocationId.toString()

}
