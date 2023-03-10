import com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar

plugins {
    scala
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

    val scalaTestVersion = "3.2.15"

    implementation("org.scala-lang:scala3-library_3:3.2.2")

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
    testImplementation("org.scalatest:scalatest_3:${scalaTestVersion}")
}

tasks.withType<ShadowJar> {
    archiveBaseName.set("${artifactName}-${artifactVersion}")
    mergeServiceFiles()
    manifest {
        attributes(mapOf("Main-Class" to "club.datatalks.kafka.Application"))
    }
    isZip64 = true
}

testing {
    suites {
        // Configure the built-in test suite
        val test by getting(JvmTestSuite::class) {
            // Use JUnit4 test framework
            useJUnit("4.13.2")

            dependencies {
                // Use Scalatest for testing our library
                implementation("org.scalatest:scalatest_2.13:3.2.13")
                implementation("org.scalatestplus:junit-4-13_2.13:3.2.2.0")

                // Need scala-xml at test runtime
                runtimeOnly("org.scala-lang.modules:scala-xml_2.13:1.2.0")
            }
        }
    }
}
