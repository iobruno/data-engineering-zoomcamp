package club.datatalks.kafka.infrastructure

import io.confluent.kafka.serializers.KafkaJsonSerializer
import org.apache.kafka.clients.producer.KafkaProducer
import org.apache.kafka.clients.producer.ProducerConfig.*
import org.apache.kafka.clients.producer.ProducerRecord
import org.apache.kafka.common.serialization.StringSerializer
import java.util.*

interface KafkaSerializable {
    fun messageKey(): String
}

class KafkaJsonProducer<T> where T : KafkaSerializable {

    private val producerConfig: Properties by lazy {
        val properties = Properties()
        properties[BOOTSTRAP_SERVERS_CONFIG] = "localhost:9090,localhost:9091,localhost:9092"
        properties[CLIENT_DNS_LOOKUP_CONFIG] = "use_all_dns_ips"
        properties[ACKS_CONFIG] = "all"
        properties[KEY_SERIALIZER_CLASS_CONFIG] = StringSerializer::class.java
        properties[VALUE_SERIALIZER_CLASS_CONFIG] = KafkaJsonSerializer::class.java
        properties
    }

    private val jsonProducer: KafkaProducer<String ,T> by lazy {
        KafkaProducer(producerConfig)
    }

    fun push(entities: Iterable<T>, topic: String) {
        val records: List<ProducerRecord<String, T>> = entities.map { ProducerRecord(topic, it.messageKey(), it) }
        records.forEach {
            jsonProducer.send(it)
        }
    }

}
