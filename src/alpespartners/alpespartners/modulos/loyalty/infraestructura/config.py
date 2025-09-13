import os
from .despachadores import FabricaDespachadorLoyalty

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')

def get_loyalty_kafka_producer():
    """
    Función para obtener el despachador de eventos de Loyalty Service.
    Usado por dependency injection en FastAPI.
    """
    return FabricaDespachadorLoyalty.crear_despachador_kafka(KAFKA_BOOTSTRAP_SERVERS)

TOPICS = {
    'EMBAJADORES_EVENTOS': 'loyalty.embajadores.eventos',
    'REFERIDOS_EVENTOS': 'loyalty.referidos.eventos'
}