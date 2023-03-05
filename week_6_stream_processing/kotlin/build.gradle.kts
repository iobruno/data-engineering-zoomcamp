import org.jetbrains.kotlin.gradle.tasks.KotlinCompile
import com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar

plugins {
    kotlin("jvm") version "1.8.10"
    id("com.github.johnrengelman.shadow") version "8.1.0"
}

val artifactName = "kafka-stream-processing"
val artifactVersion = "1.0-SNAPSHOT"

repositories {
    mavenLocal()
    mavenCentral()
    maven {
        name = "Confluent Maven Repository"
        url = uri("https://packages.confluent.io/maven/")
    }
}

dependencies {
    val confluentKafkaVersion = "7.3.2"
    val avroVersion = "1.11.1"
    val protobufVersion = "3.22.0"
    val openCsvVersion = "5.7.1"

    val junitVersion = "5.9.2"
    val mockKVersion = "1.13.4"
    val kotestVersion = "5.5.5"

    implementation("org.apache.kafka:kafka-clients:${confluentKafkaVersion}-ccs")
    implementation("org.apache.kafka:kafka-streams:${confluentKafkaVersion}-ccs")
    implementation("io.confluent:kafka-schema-registry-client:${confluentKafkaVersion}")

    /** Kafka and Kafka Streams Serde for Avro **/
    implementation("io.confluent:kafka-avro-serializer:${confluentKafkaVersion}")
    implementation("io.confluent:kafka-streams-avro-serde:${confluentKafkaVersion}")
    implementation("org.apache.avro:avro:${avroVersion}")

    /** Kafka and Kafka Streams Serde for Protobuf **/
    implementation("io.confluent:kafka-protobuf-serializer:${confluentKafkaVersion}")
    implementation("io.confluent:kafka-streams-protobuf-serde:${confluentKafkaVersion}")
    implementation("com.google.protobuf:protobuf-java:$protobufVersion")

    /** Kafka and Kafka Streams Serde for JSON Schema **/
    implementation("io.confluent:kafka-json-serializer:${confluentKafkaVersion}")
    implementation("io.confluent:kafka-streams-json-schema-serde:${confluentKafkaVersion}")

    /** CSV Parser **/
    implementation("com.opencsv:opencsv:${openCsvVersion}")

    /** Unit and Integration Test Frameworks **/
    testImplementation("org.apache.kafka:kafka-streams-test-utils:${confluentKafkaVersion}-ccs")
    testImplementation("org.junit.jupiter:junit-jupiter:$junitVersion")
    testImplementation("io.mockk:mockk:$mockKVersion")
    testImplementation("io.kotest:kotest-assertions-core-jvm:$kotestVersion")
}

tasks.withType<ShadowJar> {
    archiveBaseName.set("${artifactName}-${artifactVersion}")
    mergeServiceFiles()
    manifest {
        attributes(mapOf("Main-Class" to "club.datatalks.kafka.ApplicationKt"))
    }
    isZip64 = true
}

tasks.withType<KotlinCompile> {
    kotlinOptions {
        jvmTarget = "17"
    }
}

tasks.withType<Test> {
    useJUnitPlatform()
}
