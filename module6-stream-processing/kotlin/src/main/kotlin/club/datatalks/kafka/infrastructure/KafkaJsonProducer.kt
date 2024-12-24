package club.datatalks.kafka.infrastructure

import io.confluent.kafka.serializers.KafkaJsonSerializer
import org.apache.kafka.clients.producer.KafkaProducer
import org.apache.kafka.clients.producer.ProducerConfig
import org.apache.kafka.clients.producer.ProducerRecord
import org.apache.kafka.clients.producer.RecordMetadata
import org.apache.kafka.common.serialization.StringSerializer
import java.util.Properties
import java.util.concurrent.Future


class KafkaJsonProducer<T>
    where T : KafkaSerializable {

    private val producerConfig: Properties by lazy {
        val properties = Properties()
        properties[ProducerConfig.BOOTSTRAP_SERVERS_CONFIG] = "localhost:9092"
        properties[ProducerConfig.CLIENT_DNS_LOOKUP_CONFIG] = "use_all_dns_ips"
        properties[ProducerConfig.ACKS_CONFIG] = "all"
        properties[ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG] = StringSerializer::class.java
        properties[ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG] = KafkaJsonSerializer::class.java
        properties
    }

    private val jsonProducer: KafkaProducer<String, T> =
        KafkaProducer(producerConfig)

    fun push(entities: List<T>, topic: String): List<Future<RecordMetadata>> =
        entities
            .map { ProducerRecord(topic, it.messageKey(), it) }
            .mapNotNull { record -> jsonProducer.send(record) }
}
