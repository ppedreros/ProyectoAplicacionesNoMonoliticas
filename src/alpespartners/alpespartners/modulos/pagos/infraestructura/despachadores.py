import json
import logging
from datetime import datetime
from typing import Dict, Any

from ....seedwork.dominio.eventos import Despachador
from ..dominio.eventos import PagoIniciado, PagoProcesado, PagoFallido, ComisionPagada, ComisionRevertida

logger = logging.getLogger(__name__)

class DespachadorEventosPago(Despachador):
    """Despachador específico para eventos de pago"""
    
    def __init__(self, pulsar_client, topic_pagos: str):
        self.pulsar_client = pulsar_client
        self.topic_pagos = topic_pagos
        self.producer = pulsar_client.create_producer(topic_pagos)
    
    def publicar_evento(self, evento) -> None:
        """Publica un evento de pago a Pulsar"""
        try:
            # Serializar evento a JSON
            evento_data = self._serializar_evento(evento)
            
            # Publicar a Pulsar
            self.producer.send(
                json.dumps(evento_data).encode('utf-8'),
                properties={
                    'evento_tipo': evento.__class__.__name__,
                    'timestamp': datetime.now().isoformat(),
                    'version': '1.0'
                }
            )
            
            logger.info(f"Evento {evento.__class__.__name__} publicado exitosamente")
            
        except Exception as e:
            logger.error(f"Error publicando evento {evento.__class__.__name__}: {str(e)}")
            raise
    
    def _serializar_evento(self, evento) -> Dict[str, Any]:
        """Serializa un evento de dominio a diccionario"""
        evento_data = {
            'evento_id': str(evento.id) if hasattr(evento, 'id') else None,
            'evento_tipo': evento.__class__.__name__,
            'timestamp': evento.timestamp.isoformat() if hasattr(evento, 'timestamp') else datetime.now().isoformat(),
            'version': '1.0'
        }
        
        # Agregar datos específicos del evento
        if isinstance(evento, PagoIniciado):
            evento_data.update({
                'id_pago': evento.id_pago,
                'id_embajador': evento.id_embajador,
                'id_partner': evento.id_partner,
                'id_conversion': evento.id_conversion,
                'monto': evento.monto,
                'moneda': evento.moneda,
                'tipo_pago': evento.tipo_pago,
                'informacion_pago': evento.informacion_pago,
                'detalle_comision': evento.detalle_comision
            })
        
        elif isinstance(evento, PagoProcesado):
            evento_data.update({
                'id_pago': evento.id_pago,
                'id_embajador': evento.id_embajador,
                'id_partner': evento.id_partner,
                'id_conversion': evento.id_conversion,
                'monto': evento.monto,
                'moneda': evento.moneda,
                'id_transaccion_externa': evento.id_transaccion_externa
            })
        
        elif isinstance(evento, PagoFallido):
            evento_data.update({
                'id_pago': evento.id_pago,
                'id_embajador': evento.id_embajador,
                'id_partner': evento.id_partner,
                'id_conversion': evento.id_conversion,
                'monto': evento.monto,
                'moneda': evento.moneda,
                'motivo_fallo': evento.motivo_fallo
            })
        
        elif isinstance(evento, ComisionPagada):
            evento_data.update({
                'id_pago': evento.id_pago,
                'id_embajador': evento.id_embajador,
                'id_partner': evento.id_partner,
                'id_conversion': evento.id_conversion,
                'monto_comision': evento.monto_comision,
                'moneda': evento.moneda,
                'id_transaccion_externa': evento.id_transaccion_externa
            })
        
        elif isinstance(evento, ComisionRevertida):
            evento_data.update({
                'id_pago': evento.id_pago,
                'id_embajador': evento.id_embajador,
                'id_partner': evento.id_partner,
                'id_conversion': evento.id_conversion,
                'monto_comision': evento.monto_comision,
                'moneda': evento.moneda,
                'motivo_reversion': evento.motivo_reversion
            })
        
        return evento_data
    
    def cerrar(self) -> None:
        """Cierra el producer de Pulsar"""
        if self.producer:
            self.producer.close()
