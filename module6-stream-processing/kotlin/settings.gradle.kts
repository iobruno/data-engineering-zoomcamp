pluginManagement {
    val kotlinVersion: String by settings
    val detektVersion: String by settings
    val shadowJarVersion: String by settings

    plugins {
        kotlin("jvm") version kotlinVersion
        id("io.gitlab.arturbosch.detekt") version detektVersion
        id("com.github.johnrengelman.shadow") version shadowJarVersion
    }

}

rootProject.name = "kotlin-sp"
