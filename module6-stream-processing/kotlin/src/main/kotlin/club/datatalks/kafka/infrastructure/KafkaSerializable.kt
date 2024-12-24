package club.datatalks.kafka.infrastructure

interface KafkaSerializable {

    fun messageKey(): String?
}
