from dataclasses import asdict
from kafka import KafkaProducer
import json
import logging

from ....seedwork.dominio.eventos import EventoDominio, Despachador
from ..dominio.eventos import EmbajadorCreado, ReferidoRegistrado

logger = logging.getLogger(__name__)

class DespachadorEventosKafkaLoyalty(Despachador):
    """Despachador de eventos específico para el Loyalty Service. Publica eventos a los tópicos correspondientes en Kafka."""
    
    def __init__(self, producer: KafkaProducer):
        self.producer = producer
        self.topic_por_evento = {
            EmbajadorCreado: "loyalty.embajadores.eventos",
            ReferidoRegistrado: "loyalty.referidos.eventos"
        }

    def publicar_evento(self, evento: EventoDominio):
        try:
            topic = self.topic_por_evento.get(type(evento))
            if not topic:
                logger.warning(f"No hay topic configurado para el evento {type(evento)}")
                return

            evento_dict = asdict(evento)
            
            if 'timestamp' in evento_dict:
                evento_dict['timestamp'] = evento_dict['timestamp'].isoformat()
            if 'fecha' in evento_dict:
                evento_dict['fecha'] = evento_dict['fecha'].isoformat()
            if 'fecha_registro' in evento_dict:
                evento_dict['fecha_registro'] = evento_dict['fecha_registro'].isoformat()

            mensaje_kafka = {
                'evento_tipo': evento.__class__.__name__,
                'evento_id': evento.id,
                'servicio_origen': 'loyalty',
                'version': '1.0',
                'datos': evento_dict
            }

            self.producer.send(
                topic,
                value=mensaje_kafka
            )
            
            self.producer.flush()
            
            logger.info(f"Evento {evento.__class__.__name__} publicado en topic {topic}")
            
        except Exception as e:
            logger.error(f"Error publicando evento {type(evento)}: {str(e)}")
            raise


class FabricaDespachadorLoyalty:
    """Fábrica para crear el despachador de eventos del Loyalty Service."""
    
    @staticmethod
    def crear_despachador_kafka(bootstrap_servers: str = 'localhost:9092') -> DespachadorEventosKafkaLoyalty:
        try:
            producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                acks='all',  # Esperar confirmación de todos los brokers
                retries=3,   # Reintentar en caso de falla
                max_in_flight_requests_per_connection=1  # Mantener orden
            )
            
            return DespachadorEventosKafkaLoyalty(producer)
            
        except Exception as e:
            logger.error(f"Error creando despachador Kafka: {str(e)}")
            raise