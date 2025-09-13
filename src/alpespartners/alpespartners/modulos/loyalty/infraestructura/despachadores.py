import json
import logging
import pulsar
from datetime import datetime

from alpespartners.config.pulsar import get_pulsar_client, TOPICS

logger = logging.getLogger(__name__)

class DespachadorEventosPulsarLoyalty:
    def __init__(self):
        self.client = get_pulsar_client()
        self.producers = {}
        
    def _get_producer(self, topic: str):
        if topic not in self.producers:
            self.producers[topic] = self.client.create_producer(topic)
        return self.producers[topic]
    
    def publicar_evento(self, evento, canal: str = None):
        "Método genérico requerido por ServicioLoyalty"
        try:
            logger.info(f"📤 Publicando evento: {type(evento).__name__}")
            
            if hasattr(evento, "nombre_evento"):
                evento_tipo = evento.nombre_evento
            else:
                evento_tipo = type(evento).__name__
            
            if "Referido" in evento_tipo or "ReferidoRegistrado" in evento_tipo:
                return self.publicar_evento_referido_registrado(evento)
            else:
                return self.publicar_evento_embajador_creado(evento)
                
        except Exception as e:
            logger.error(f"❌ Error publicando evento: {str(e)}")
            return False
    
    def publicar_evento_referido_registrado(self, evento):
        try:
            topic = TOPICS["LOYALTY_REFERIDOS"]
            producer = self._get_producer(topic)
            
            datos_evento = {
                "id_referido": getattr(evento, "id_referido", ""),
                "id_embajador": getattr(evento, "id_embajador", ""),
                "email_referido": getattr(evento, "email_referido", ""),
                "nombre_referido": getattr(evento, "nombre_referido", ""),
                "valor_conversion": getattr(evento, "valor_conversion", 0.0),
                "porcentaje_comision": getattr(evento, "porcentaje_comision", 5.0),
                "timestamp": datetime.utcnow().isoformat(),
                "id_partner": "loyalty-partner"
            }
            
            mensaje = {
                "evento_tipo": "ReferidoRegistrado",
                "servicio_origen": "loyalty",
                "timestamp": datetime.utcnow().isoformat(),
                "version": "1.0",
                "datos": datos_evento
            }
            
            message_id = producer.send(json.dumps(mensaje).encode("utf-8"))
            logger.info(f"📤 ReferidoRegistrado enviado: {datos_evento.get('id_referido')}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error enviando evento referido: {str(e)}")
            return False
    
    def publicar_evento_embajador_creado(self, evento):
        # Implementación básica
        logger.info("📤 EmbajadorCreado (simulado)")
        return True
    
    def close(self):
        for producer in self.producers.values():
            producer.close()
        self.client.close()

class FabricaDespachadorLoyalty:
    @staticmethod
    def crear_despachador_pulsar():
        return DespachadorEventosPulsarLoyalty()