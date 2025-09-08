from dataclasses import asdict
from kafka import KafkaProducer
import json

from ....seedwork.dominio.eventos import EventoDominio, Despachador
from ..dominio.eventos import ClickRegistrado, ConversionRegistrada, AtribucionAsignada
from ....config.kafka import TOPIC_CLICKS, TOPIC_CONVERSIONES, TOPIC_ATRIBUCIONES

class DespachadorEventosKafka(Despachador):
    def __init__(self, producer: KafkaProducer):
        self.producer = producer
        self.topic_por_evento = {
            ClickRegistrado: TOPIC_CLICKS,
            ConversionRegistrada: TOPIC_CONVERSIONES,
            AtribucionAsignada: TOPIC_ATRIBUCIONES
        }

    def publicar_evento(self, evento: EventoDominio):
        # Obtener el topic correspondiente al tipo de evento
        topic = self.topic_por_evento.get(type(evento))
        if not topic:
            raise ValueError(f"No hay topic configurado para el evento {type(evento)}")

        # Convertir el evento a diccionario y serializar
        evento_dict = asdict(evento)
        # Convertir datetime a string ISO
        if 'timestamp' in evento_dict:
            evento_dict['timestamp'] = evento_dict['timestamp'].isoformat()
        if 'fecha' in evento_dict:
            evento_dict['fecha'] = evento_dict['fecha'].isoformat()

        # Publicar en Kafka
        self.producer.send(
            topic,
            value=evento_dict
        )
