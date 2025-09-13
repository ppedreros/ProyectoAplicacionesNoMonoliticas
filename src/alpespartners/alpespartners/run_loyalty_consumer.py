"""
Script para ejecutar el consumer de eventos de Loyalty Service.
Este script escucha eventos ReferidoRegistrado y los procesa en Tracking Service.
"""

import os
import sys
import time
import signal
from sqlalchemy.orm import Session

# Agregar el path del proyecto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from alpespartners.config.database import get_db
from alpespartners.modulos.tracking.infraestructura.consumidores import ConsumidorEventosLoyalty

def main():
    """
    Función principal que ejecuta el consumer de eventos de Loyalty.
    """
    print("Iniciando Consumer de Eventos Loyalty → Tracking")
    print("=" * 60)
    
    # Crear consumer
    consumer = ConsumidorEventosLoyalty(get_db)
    
    # Configurar manejador de señales para cierre limpio
    def signal_handler(signum, frame):
        print(f"\nRecibida señal {signum}. Cerrando consumer...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        print("Esperando que Kafka esté disponible...")
        time.sleep(5)
        
        print("Inicializando conexión a Kafka...")
        consumer.inicializar_consumer()
        
        print("Consumer listo. Escuchando eventos de Loyalty Service...")
        print("   - Topic: loyalty.referidos.eventos")
        print("   - Eventos esperados: ReferidoRegistrado")
        print("   - Presiona Ctrl+C para detener")
        print("=" * 60)
        
        # Procesar eventos (este método bloquea)
        consumer.procesar_eventos()
        
    except KeyboardInterrupt:
        print("\nConsumer detenido por el usuario.")
    except Exception as e:
        print(f"\nError fatal: {str(e)}")
        sys.exit(1)
    finally:
        print("Consumer finalizado.")

if __name__ == "__main__":
    main()