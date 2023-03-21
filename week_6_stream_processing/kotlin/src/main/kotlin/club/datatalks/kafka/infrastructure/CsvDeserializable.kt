package club.datatalks.kafka.infrastructure

import com.fasterxml.jackson.dataformat.csv.CsvMapper
import com.fasterxml.jackson.dataformat.csv.CsvSchema
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule
import com.fasterxml.jackson.module.kotlin.KotlinModule
import java.io.BufferedReader

interface CsvDeserializable<T> {

    companion object {
        inline fun <reified T> listFromCsv(reader: BufferedReader, schema: CsvSchema, containsHeader: Boolean = true): List<T> {
            val csvSchema = if (containsHeader)
                schema.withHeader()
            else
                schema.withoutHeader()

            val mapper = CsvMapper()
                .registerModule(KotlinModule.Builder().build())
                .registerModule(JavaTimeModule())

            return mapper
                .readerFor(T::class.java)
                .with(csvSchema)
                .readValues<T>(reader)
                .readAll()!!
        }
    }

}