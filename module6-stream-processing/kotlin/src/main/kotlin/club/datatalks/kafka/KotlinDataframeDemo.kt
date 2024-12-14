package club.datatalks.kafka

import club.datatalks.kafka.dto.GreenTaxiDTO
import org.jetbrains.kotlinx.dataframe.DataFrame
import org.jetbrains.kotlinx.dataframe.annotations.DataSchema
import org.jetbrains.kotlinx.dataframe.api.ColumnsSelectionDsl
import org.jetbrains.kotlinx.dataframe.api.column
import org.jetbrains.kotlinx.dataframe.api.into
import org.jetbrains.kotlinx.dataframe.api.rename
import org.jetbrains.kotlinx.dataframe.api.toList
import org.jetbrains.kotlinx.dataframe.api.toListOf
import org.jetbrains.kotlinx.dataframe.io.readCSV
import java.io.BufferedReader
import java.io.InputStream
import java.nio.file.Path
import java.nio.file.Paths

@DataSchema
data class Popcorn(val flavor1: String, val flavor2: String, val flavor3: String)





object KotlinDataframeDemo {

    fun readCsv(file: Path, containsHeader: Boolean = true) {
        val url = file.toString()
        val df = DataFrame.readCSV(file.toString(), skipLines = 1, header = listOf("flavor1", "flavor2", "flavor3"))


        println(df)
    }
}

fun main() {
    val file: Path = Paths.get("/Users/iobruno/Vault/data-engineering-zoomcamp/module6-stream-processing/kotlin/src/main/resources/popcorn.csv")

    KotlinDataframeDemo.readCsv(file)
}
