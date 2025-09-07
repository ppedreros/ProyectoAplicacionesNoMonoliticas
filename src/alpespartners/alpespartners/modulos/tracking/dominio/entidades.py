from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from .objetos_valor import MetadataCliente, InformacionMonetaria, DatosAtribucion, TipoConversion
from .eventos import ClickRegistrado, ConversionRegistrada, AtribucionAsignada

@dataclass
class Entidad:
    id: str = field(default_factory=lambda: str(uuid4()))

@dataclass
class AgregacionRaiz(Entidad):
    eventos: List = field(default_factory=list)

    def agregar_evento(self, evento):
        self.eventos.append(evento)

@dataclass
class Click(Entidad):
    id_partner: str = field(default=None)
    id_campana: str = field(default=None)
    url_origen: str = field(default=None)
    url_destino: str = field(default=None)
    timestamp: datetime = field(default_factory=datetime.now)
    metadata_cliente: MetadataCliente = field(default=None)

    @property
    def id_click(self) -> str:
        return self.id

@dataclass
class Conversion(AgregacionRaiz):
    id_conversion: str = field(default=None)
    id_click: Optional[str] = field(default=None)
    id_partner: str = field(default=None)
    id_campana: str = field(default=None)
    tipo: TipoConversion = field(default=None)
    informacion_monetaria: InformacionMonetaria = field(default=None)
    timestamp: datetime = field(default_factory=datetime.now)
    metadata_cliente: MetadataCliente = field(default=None)
    atribuciones: List[DatosAtribucion] = field(default_factory=list)

    def registrar_conversion(self):
        evento = ConversionRegistrada(
            id_conversion=self.id_conversion,
            id_click=self.id_click,
            id_partner=self.id_partner,
            id_campana=self.id_campana,
            tipo_conversion=self.tipo.value,
            valor=self.informacion_monetaria.valor,
            comision=self.informacion_monetaria.comision,
            timestamp=self.timestamp,
            metadata_cliente=self.metadata_cliente.__dict__
        )
        self.agregar_evento(evento)

    def asignar_atribucion(self, datos_atribucion: DatosAtribucion):
        self.atribuciones.append(datos_atribucion)
        evento = AtribucionAsignada(
            id_atribucion=str(len(self.atribuciones)),
            id_conversion=self.id_conversion,
            id_partner=self.id_partner,
            id_campana=self.id_campana,
            modelo_atribucion=datos_atribucion.modelo.value,
            porcentaje_atribucion=datos_atribucion.porcentaje,
            timestamp=datos_atribucion.timestamp
        )
        self.agregar_evento(evento)

