import os
import pulsar

PULSAR_SERVICE_URL = os.getenv("PULSAR_SERVICE_URL", "pulsar://pulsar:6650")
PULSAR_ADMIN_URL = os.getenv("PULSAR_ADMIN_URL", "http://pulsar:8080")

TOPICS = {
    "LOYALTY_REFERIDOS": "persistent://public/default/loyalty-referidos-eventos",
    "PAGOS_EVENTOS": "persistent://public/default/pagos-eventos",
    "PAGOS_COMANDOS": "persistent://public/default/pagos-comandos",
    "AFILIADOS_EVENTOS": "persistent://public/default/afiliados-eventos",
    "AFILIADOS_COMANDOS": "persistent://public/default/afiliados-comandos",
    "COMANDO_REGISTRAR_CLICK": "persistent://public/default/comando-registrar-click",
    "COMANDO_REGISTRAR_CONVERSION": "persistent://public/default/comando-registrar-conversion", 
    "COMANDO_CREAR_AFILIADO": "persistent://public/default/comando-crear-afiliado",
    "COMANDO_CREAR_PAGO": "persistent://public/default/comando-crear-pago"
}

def get_pulsar_client():
    """Crea un cliente de Pulsar con configuración de error handling"""
    try:
        client = pulsar.Client(
            PULSAR_SERVICE_URL,
            connection_timeout_ms=5000,  # 5 segundos timeout
        )
        return client
    except Exception as e:
        print(f"Error creando cliente de Pulsar: {str(e)}")
        return None
