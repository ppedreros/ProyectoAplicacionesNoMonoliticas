from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict
from uuid import uuid4

@dataclass
class EventoDominio:
    id: str = field(default_factory=lambda: str(uuid4()))
    fecha_evento: datetime = field(default_factory=datetime.now)

@dataclass
class ClickRegistrado(EventoDominio):
    id_click: str = field(default=None)
    id_partner: str = field(default=None)
    id_campana: str = field(default=None)
    url_origen: str = field(default=None)
    url_destino: str = field(default=None)
    timestamp: datetime = field(default_factory=datetime.now)
    metadata_cliente: Dict = field(default_factory=dict)

@dataclass
class ConversionRegistrada(EventoDominio):
    id_conversion: str = field(default=None)
    id_click: str = field(default=None)
    id_partner: str = field(default=None)
    id_campana: str = field(default=None)
    tipo_conversion: str = field(default=None)
    valor: float = field(default=0.0)
    comision: float = field(default=0.0)
    timestamp: datetime = field(default_factory=datetime.now)
    metadata_cliente: Dict = field(default_factory=dict)

@dataclass
class AtribucionAsignada(EventoDominio):
    id_atribucion: str = field(default=None)
    id_conversion: str = field(default=None)
    id_partner: str = field(default=None)
    id_campana: str = field(default=None)
    modelo_atribucion: str = field(default=None)
    porcentaje_atribucion: float = field(default=0.0)
    timestamp: datetime = field(default_factory=datetime.now)