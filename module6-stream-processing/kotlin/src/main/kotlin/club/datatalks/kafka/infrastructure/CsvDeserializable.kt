package club.datatalks.kafka.infrastructure

import com.fasterxml.jackson.dataformat.csv.CsvMapper
import com.fasterxml.jackson.dataformat.csv.CsvSchema
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule
import com.fasterxml.jackson.module.kotlin.KotlinModule
import java.io.BufferedReader
import java.nio.file.Files
import java.nio.file.Path

interface CsvDeserializable<T> {

    companion object {
        inline fun <reified T> seqFromCsv(
            filepath: Path,
            schema: CsvSchema,
            containsHeader: Boolean = true
        ): Sequence<T> {
            val reader = Files.newBufferedReader(filepath)!!

            val csvSchema =
                if (containsHeader) schema.withHeader()
                else schema.withoutHeader()

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
