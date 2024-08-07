import com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar
import org.jetbrains.kotlin.gradle.dsl.JvmTarget
import org.jetbrains.kotlin.gradle.tasks.KotlinJvmCompile
import io.gitlab.arturbosch.detekt.Detekt

plugins {
    kotlin("jvm") version "2.0.0"
    id("com.github.johnrengelman.shadow") version "8.1.1"
    id("io.gitlab.arturbosch.detekt") version("1.23.6")
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
    val confluentKafkaVersion = "7.6.1"
    val protobufVersion = "4.27.2"
    val avroVersion = "1.11.3"
    val jacksonVersion = "2.17.2"
    val picocliVersion = "4.7.6"

    val kotlinLoggingVersion = "7.0.0"
    val logbackVersion = "1.5.6"

    val kotestVersion = "5.9.1"
    val mockKVersion = "1.13.11"
    val junitVersion = "5.10.3"

    implementation("org.apache.kafka:kafka-clients:${confluentKafkaVersion}-ccs")
    implementation("org.apache.kafka:kafka-streams:${confluentKafkaVersion}-ccs")
    implementation("io.confluent:kafka-schema-registry-client:${confluentKafkaVersion}")

    /** Kafka and Kafka Streams Serde for Protobuf **/
    implementation("io.confluent:kafka-protobuf-serializer:${confluentKafkaVersion}")
    implementation("io.confluent:kafka-streams-protobuf-serde:${confluentKafkaVersion}")
    implementation("com.google.protobuf:protobuf-java:$protobufVersion")

    /** Kafka and Kafka Streams Serde for JSON Schema **/
    implementation("io.confluent:kafka-json-serializer:${confluentKafkaVersion}")
    implementation("io.confluent:kafka-streams-json-schema-serde:${confluentKafkaVersion}")

    /** Kafka and Kafka Streams Serde for Avro **/
    implementation("io.confluent:kafka-avro-serializer:${confluentKafkaVersion}")
    implementation("io.confluent:kafka-streams-avro-serde:${confluentKafkaVersion}")
    implementation("org.apache.avro:avro:${avroVersion}")

    /** CLI Builder **/
    implementation("info.picocli:picocli:$picocliVersion")

    /** CSV Parser **/
    implementation("com.fasterxml.jackson.dataformat:jackson-dataformat-csv:${jacksonVersion}")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin:${jacksonVersion}")
    implementation("com.fasterxml.jackson.datatype:jackson-datatype-jsr310:${jacksonVersion}")

    /** Logging **/
    implementation("io.github.oshai:kotlin-logging-jvm:${kotlinLoggingVersion}")
    implementation("ch.qos.logback:logback-classic:${logbackVersion}")

    /** Unit and Integration Test Frameworks **/
    testImplementation("org.apache.kafka:kafka-streams-test-utils:${confluentKafkaVersion}-ccs")
    testImplementation("io.kotest:kotest-assertions-core-jvm:$kotestVersion")
    testImplementation("io.mockk:mockk:$mockKVersion")
    testImplementation("org.junit.jupiter:junit-jupiter:$junitVersion")
}

detekt {
    toolVersion = "1.23.6"
    config.setFrom(file("detekt.yml"))
    buildUponDefaultConfig = true
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

tasks.withType<KotlinJvmCompile>().configureEach {
    compilerOptions {
        jvmTarget.set(JvmTarget.JVM_21)
        freeCompilerArgs.add("-opt-in=kotlin.RequiresOptIn")
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

tasks.withType<Test> {
    useJUnitPlatform()
}
