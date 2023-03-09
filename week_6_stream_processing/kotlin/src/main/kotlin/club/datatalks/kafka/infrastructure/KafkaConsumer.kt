package club.datatalks.kafka.infrastructure

import club.datatalks.kafka.dto.RideDTO
import io.confluent.kafka.serializers.KafkaJsonDeserializer
import io.confluent.kafka.serializers.KafkaJsonDeserializerConfig
import org.apache.kafka.clients.consumer.ConsumerConfig.*
import org.apache.kafka.clients.consumer.ConsumerRecords
import org.apache.kafka.clients.consumer.KafkaConsumer
import org.apache.kafka.common.serialization.StringDeserializer
import java.time.Duration
import java.util.Properties


class KafkaJsonConsumer<T> {

    private val consumerConfig: Properties by lazy {
        val properties = Properties()
        properties[BOOTSTRAP_SERVERS_CONFIG] = "localhost:9090,localhost:9091,localhost:9092"
        properties[CLIENT_DNS_LOOKUP_CONFIG] = "use_all_dns_ips"
        properties[SESSION_TIMEOUT_MS_CONFIG] = "45000"
        properties[ENABLE_AUTO_COMMIT_CONFIG] = false
        properties[AUTO_OFFSET_RESET_CONFIG] = "earliest"
        properties[GROUP_ID_CONFIG] = "kafkaConsumerGroup"
        properties[KEY_DESERIALIZER_CLASS_CONFIG] = StringDeserializer::class.java
        properties[VALUE_DESERIALIZER_CLASS_CONFIG] = KafkaJsonDeserializer::class.java

        //TODO: Switch to reified functions
        properties[KafkaJsonDeserializerConfig.JSON_KEY_TYPE] = RideDTO::class.java
        properties
    }

    private val jsonConsumer : KafkaConsumer<String, T> by lazy {
        KafkaConsumer<String, T>(consumerConfig)
    }

    fun subscribeTo(topic: String) {
        jsonConsumer.subscribe(listOf(topic))
        while (true) {
            val kafkaRecord: ConsumerRecords<String, T>? = jsonConsumer.poll(Duration.ofSeconds(5L))
            val records: List<T> = kafkaRecord?.map { it.value() }.orEmpty()
            records.forEach { println(it) }
        }
    }

}
