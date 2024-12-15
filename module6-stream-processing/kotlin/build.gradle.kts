import com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar
import io.gitlab.arturbosch.detekt.Detekt

plugins {
    kotlin("jvm")
    id("io.gitlab.arturbosch.detekt")
    id("com.github.johnrengelman.shadow")
}

val artifactName = "kotlin-sp"
val artifactVersion = "2.0-SNAPSHOT"

repositories {
    mavenLocal()
    mavenCentral()
    maven {
        name = "Confluent Maven Repository"
        url = uri("https://packages.confluent.io/maven/")
    }
}

dependencies {
    val kotlinDataframeVersion: String by project
    val confluentKafkaVersion: String by project
    val protobufVersion: String by project
    val avroVersion: String by project
    val jacksonVersion: String by project
    val picocliVersion: String by project
    val kotlinLoggingVersion: String by project
    val logbackVersion: String by project
    val kotestVersion: String by project
    val mockKVersion: String by project

    implementation("org.jetbrains.kotlinx:dataframe-csv:${kotlinDataframeVersion}")
    implementation("org.apache.kafka:kafka-clients:${confluentKafkaVersion}-ccs")
    implementation("org.apache.kafka:kafka-streams:${confluentKafkaVersion}-ccs")
    implementation("io.confluent:kafka-schema-registry-client:${confluentKafkaVersion}")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin:${jacksonVersion}")
    implementation("com.fasterxml.jackson.datatype:jackson-datatype-jsr310:${jacksonVersion}")
    implementation("com.fasterxml.jackson.dataformat:jackson-dataformat-csv:${jacksonVersion}")
    implementation("info.picocli:picocli:$picocliVersion")

    /** Kafka and Kafka Streams Serde for Protobuf **/
    implementation("io.confluent:kafka-protobuf-serializer:${confluentKafkaVersion}")
    implementation("io.confluent:kafka-streams-protobuf-serde:${confluentKafkaVersion}")
    implementation("com.google.protobuf:protobuf-kotlin:$protobufVersion")

    /** Kafka and Kafka Streams Serde for JSON Schema **/
    implementation("io.confluent:kafka-json-serializer:${confluentKafkaVersion}")
    implementation("io.confluent:kafka-streams-json-schema-serde:${confluentKafkaVersion}")

    /** Kafka and Kafka Streams Serde for Avro **/
    implementation("io.confluent:kafka-avro-serializer:${confluentKafkaVersion}")
    implementation("io.confluent:kafka-streams-avro-serde:${confluentKafkaVersion}")
    implementation("org.apache.avro:avro:${avroVersion}")

    /** Logging **/
    implementation("io.github.oshai:kotlin-logging-jvm:${kotlinLoggingVersion}")
    implementation("ch.qos.logback:logback-classic:${logbackVersion}")

    /** Unit and Integration Test Frameworks **/
    testImplementation("org.apache.kafka:kafka-streams-test-utils:${confluentKafkaVersion}-ccs")
    testImplementation("io.kotest:kotest-runner-junit5-jvm:$kotestVersion")
    testImplementation("io.kotest:kotest-assertions-core-jvm:$kotestVersion")
    testImplementation("io.mockk:mockk:$mockKVersion")
}

kotlin {
    jvmToolchain(21)
}

detekt {
    config.setFrom(file("detekt.yml"))
    buildUponDefaultConfig = true
}

tasks.withType<Test> {
    useJUnitPlatform()
}

tasks.withType<Detekt>().configureEach {
    reports {
        xml.required.set(true)
        html.required.set(true)
        md.required.set(true)
        txt.required.set(false)
        sarif.required.set(false)
    }
}

tasks.withType<ShadowJar> {
    manifest {
        attributes(mapOf("Main-Class" to "club.datatalks.kafka.CliApplication"))
    }
    archiveBaseName.set(artifactName)
    version = "1.0"
    archiveClassifier.set("")
    isZip64 = true
    mergeServiceFiles()
}
