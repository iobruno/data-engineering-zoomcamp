package club.datatalks.kafka.infrastructure

import io.confluent.kafka.serializers.KafkaJsonSerializer
import org.apache.kafka.clients.producer.KafkaProducer
import org.apache.kafka.clients.producer.ProducerConfig.*
import org.apache.kafka.clients.producer.ProducerRecord
import org.apache.kafka.clients.producer.RecordMetadata
import org.apache.kafka.common.serialization.StringSerializer
import java.util.*
import java.util.concurrent.Future

interface KafkaSerializable {
    fun messageKey(): String
}

class KafkaJsonProducer<T : KafkaSerializable> {

    private val producerConfig: Properties by lazy {
        val properties = Properties()
        properties[BOOTSTRAP_SERVERS_CONFIG] = "localhost:9090,localhost:9091,localhost:9092"
        properties[CLIENT_DNS_LOOKUP_CONFIG] = "use_all_dns_ips"
        properties[ACKS_CONFIG] = "1"
        properties[KEY_SERIALIZER_CLASS_CONFIG] = StringSerializer::class.java
        properties[VALUE_SERIALIZER_CLASS_CONFIG] = KafkaJsonSerializer::class.java
        properties
    }

    private val jsonProducer: KafkaProducer<String ,T> by lazy {
        KafkaProducer(producerConfig)
    }

    fun push(entities: Sequence<T>, topic: String): Sequence<Future<RecordMetadata>> {
        val producerRecords: Sequence<ProducerRecord<String, T>> = entities.map { ProducerRecord(topic, it.messageKey(), it) }
        val chunkedProducerRecords: Sequence<List<ProducerRecord<String, T>>> = producerRecords.chunked(100_000)
        val futures: Sequence<Future<RecordMetadata>> = chunkedProducerRecords.flatMap { records ->
            records.map { record -> jsonProducer.send(record) }
        }
        return futures
    }

}
