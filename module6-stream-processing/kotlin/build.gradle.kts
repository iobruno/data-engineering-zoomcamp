import com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar

plugins {
    kotlin("jvm")
    kotlin("kapt")
    id("org.graalvm.buildtools.native")
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
    val jacksonVersion: String by project
    val picocliVersion: String by project
    val kotlinLoggingVersion: String by project
    val logbackVersion: String by project

    /** CLI */
    implementation("info.picocli:picocli:$picocliVersion")
    kapt("info.picocli:picocli-codegen:$picocliVersion")

    implementation("org.jetbrains.kotlinx:dataframe-csv:${kotlinDataframeVersion}")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin:${jacksonVersion}")
    implementation("com.fasterxml.jackson.datatype:jackson-datatype-jsr310:${jacksonVersion}")
    implementation("com.fasterxml.jackson.dataformat:jackson-dataformat-csv:${jacksonVersion}")

    /** Kafka and Serde for JSON Schema **/
    implementation("org.apache.kafka:kafka-clients:${confluentKafkaVersion}-ccs")
    implementation("io.confluent:kafka-json-serializer:${confluentKafkaVersion}")

    /** Logging **/
    implementation("io.github.oshai:kotlin-logging-jvm:${kotlinLoggingVersion}")
    implementation("ch.qos.logback:logback-classic:${logbackVersion}")
}

kotlin {
    jvmToolchain(21)
}

graalvmNative {
    binaries {
        named("main") {
            mainClass.set("club.datatalks.kafka.CliApplication")
        }
    }
}

tasks.withType<Jar> {
    from("src/main/resources") {
        include("META-INF/native-image/**")
        duplicatesStrategy = DuplicatesStrategy.INCLUDE
    }
}

tasks.withType<ShadowJar> {
    manifest {
        attributes(mapOf("Main-Class" to "club.datatalks.kafka.CliApplication"))
    }
    archiveClassifier.set("")
    archiveBaseName.set(artifactName)
    version = artifactVersion
    isZip64 = true
    mergeServiceFiles()
}

tasks.withType<Test> {
    useJUnitPlatform()
}
