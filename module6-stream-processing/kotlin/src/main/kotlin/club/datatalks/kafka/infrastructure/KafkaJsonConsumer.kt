package club.datatalks.kafka.infrastructure

import io.confluent.kafka.serializers.KafkaJsonDeserializer
import io.confluent.kafka.serializers.KafkaJsonDeserializerConfig.JSON_VALUE_TYPE
import org.apache.kafka.clients.consumer.ConsumerConfig
import org.apache.kafka.clients.consumer.ConsumerRecords
import org.apache.kafka.clients.consumer.KafkaConsumer
import org.apache.kafka.common.serialization.StringDeserializer
import java.time.Duration
import java.util.Properties
import kotlin.reflect.KClass

class KafkaJsonConsumer<T>(private val deserializationClass: KClass<T>)
    where T : KafkaSerializable {

    private val consumerConfig: Properties by lazy {
        val properties = Properties()
        properties[ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG] = "localhost:9092"
        properties[ConsumerConfig.CLIENT_DNS_LOOKUP_CONFIG] = "use_all_dns_ips"
        properties[ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG] = "45000"
        properties[ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG] = false
        properties[ConsumerConfig.AUTO_OFFSET_RESET_CONFIG] = "earliest"
        properties[ConsumerConfig.GROUP_ID_CONFIG] = "defaultConsumerGroup"
        properties[ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG] = StringDeserializer::class.java
        properties[ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG] = KafkaJsonDeserializer::class.java
        properties[JSON_VALUE_TYPE] = deserializationClass.java
        properties
    }

    private val jsonConsumer: KafkaConsumer<String, T> by lazy {
        KafkaConsumer<String, T>(consumerConfig)
    }

    fun subscribeTo(
        topic: String,
        consumerGroup: String? = null,
        pollingDuration: Duration = Duration.ofSeconds(1L)
    ): ConsumerRecords<String, T> {
        if (consumerGroup != null) {
            consumerConfig[ConsumerConfig.GROUP_ID_CONFIG] = consumerGroup
        }
        jsonConsumer.subscribe(listOf(topic))
        return jsonConsumer.poll(pollingDuration)!!
    }

    fun commit() = jsonConsumer.commitSync()
}
