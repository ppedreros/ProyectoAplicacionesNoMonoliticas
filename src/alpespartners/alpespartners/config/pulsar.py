import os
import pulsar

PULSAR_SERVICE_URL = os.getenv("PULSAR_SERVICE_URL", "pulsar://pulsar:6650")
PULSAR_ADMIN_URL = os.getenv("PULSAR_ADMIN_URL", "http://pulsar:8080")

TOPICS = {
    "LOYALTY_REFERIDOS": "persistent://public/default/loyalty-referidos-eventos"
}

def get_pulsar_client():
    return pulsar.Client(PULSAR_SERVICE_URL)
