package club.datatalks.kafka.producer

import club.datatalks.kafka.dto.FhvTaxiDTO
import club.datatalks.kafka.dto.GreenTaxiDTO
import club.datatalks.kafka.dto.YellowTaxiDTO


class GreenTaxiKafkaJsonProducer(private val topic: String) :
    AbstractKafkaJsonProducer<GreenTaxiDTO>(topic)

class YellowTaxiKafkaJsonProducer(private val topic: String) :
    AbstractKafkaJsonProducer<YellowTaxiDTO>(topic)

class FhvTaxiKafkaJsonProducer(private val topic: String) :
    AbstractKafkaJsonProducer<FhvTaxiDTO>(topic)
