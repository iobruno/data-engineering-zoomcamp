package club.datatalks.kafka.infrastructure

import com.fasterxml.jackson.databind.MappingIterator
import com.fasterxml.jackson.dataformat.csv.CsvMapper
import com.fasterxml.jackson.dataformat.csv.CsvSchema
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule
import com.fasterxml.jackson.module.kotlin.KotlinModule
import java.io.BufferedReader

interface CsvDeserializable<T> {

    companion object {
        inline fun <reified T> seqFromCsv(reader: BufferedReader,
                                          schema: CsvSchema,
                                          containsHeader: Boolean = true): Sequence<T> {
            val csvSchema = if (containsHeader)
                schema.withHeader()
            else
                schema.withoutHeader()

            val mapper = CsvMapper()
                .registerModule(KotlinModule.Builder().build())
                .registerModule(JavaTimeModule())

            val entries = mapper.readerFor(T::class.java)
                .with(csvSchema)
                .readValues<T>(reader)
                .readAll()!!

            return entries.asSequence()
        }
    }

}