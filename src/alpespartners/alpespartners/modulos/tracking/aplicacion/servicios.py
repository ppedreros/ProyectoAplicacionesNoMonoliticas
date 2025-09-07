from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from ..dominio.entidades import Click, Conversion
from ..dominio.repositorios import RepositorioClicks, RepositorioConversiones
from ..dominio.objetos_valor import MetadataCliente, InformacionMonetaria, DatosAtribucion, TipoConversion, ModeloAtribucion

@dataclass
class ServicioTracking:
    repositorio_clicks: RepositorioClicks
    repositorio_conversiones: RepositorioConversiones

    def registrar_click(self, 
                       id_partner: str,
                       id_campana: str,
                       url_origen: str,
                       url_destino: str,
                       metadata_cliente: MetadataCliente) -> str:
        click = Click(
            id_partner=id_partner,
            id_campana=id_campana,
            url_origen=url_origen,
            url_destino=url_destino,
            metadata_cliente=metadata_cliente,
            timestamp=datetime.now()
        )
        self.repositorio_clicks.agregar(click)
        return click.id_click

    def registrar_conversion(self,
                           id_partner: str,
                           id_campana: str,
                           tipo: TipoConversion,
                           informacion_monetaria: InformacionMonetaria,
                           metadata_cliente: MetadataCliente,
                           id_click: Optional[str] = None) -> str:
        conversion = Conversion(
            id_partner=id_partner,
            id_campana=id_campana,
            id_click=id_click,
            tipo=tipo,
            informacion_monetaria=informacion_monetaria,
            metadata_cliente=metadata_cliente,
            timestamp=datetime.now()
        )
        conversion.registrar_conversion()
        self.repositorio_conversiones.agregar(conversion)
        return conversion.id_conversion

    def asignar_atribucion(self,
                          id_conversion: str,
                          modelo: ModeloAtribucion,
                          porcentaje: float,
                          ventana_atribucion: int):
        conversion = self.repositorio_conversiones.obtener_por_id(id_conversion)
        datos_atribucion = DatosAtribucion(
            modelo=modelo,
            porcentaje=porcentaje,
            timestamp=datetime.now(),
            ventana_atribucion=ventana_atribucion
        )
        conversion.asignar_atribucion(datos_atribucion)
        self.repositorio_conversiones.actualizar(conversion)

    def obtener_conversiones_partner(self, 
                                   id_partner: str, 
                                   desde: Optional[datetime] = None, 
                                   hasta: Optional[datetime] = None) -> List[Conversion]:
        return self.repositorio_conversiones.obtener_por_partner(id_partner, desde, hasta)

