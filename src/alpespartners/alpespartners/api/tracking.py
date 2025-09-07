from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from kafka import KafkaProducer

from ..config.database import get_db
from ..config.kafka import get_kafka_producer, TOPIC_CLICKS, TOPIC_CONVERSIONES, TOPIC_ATRIBUCIONES

class ClickRequest(BaseModel):
    id_partner: str
    id_campana: str
    url_origen: str
    url_destino: str
    metadata_cliente: Dict

class ConversionRequest(BaseModel):
    id_partner: str
    id_campana: str
    tipo_conversion: str
    informacion_monetaria: Dict
    metadata_cliente: Dict
    id_click: Optional[str] = None

class AtribucionRequest(BaseModel):
    modelo: str
    porcentaje: float
    ventana_atribucion: int

from alpespartners.modulos.tracking.aplicacion.servicios import ServicioTracking
from alpespartners.modulos.tracking.dominio.entidades import Click, Conversion
from alpespartners.modulos.tracking.dominio.objetos_valor import (
    MetadataCliente,
    InformacionMonetaria,
    TipoConversion,
    ModeloAtribucion
)
from alpespartners.modulos.tracking.infraestructura.repositorios_sql import (
    RepositorioClicksSQL,
    RepositorioConversionesSQL
)

router = APIRouter()

def get_tracking_service(db: Session = Depends(get_db)):
    repo_clicks = RepositorioClicksSQL(db)
    repo_conversiones = RepositorioConversionesSQL(db)
    return ServicioTracking(repo_clicks, repo_conversiones)

@router.post("/tracking/clicks")
async def registrar_click(
    request: ClickRequest,
    servicio_tracking: ServicioTracking = Depends(get_tracking_service),
    producer: KafkaProducer = Depends(get_kafka_producer)
) -> str:
    try:
        metadata = MetadataCliente(**request.metadata_cliente)
        click_id = servicio_tracking.registrar_click(
            id_partner=request.id_partner,
            id_campana=request.id_campana,
            url_origen=request.url_origen,
            url_destino=request.url_destino,
            metadata_cliente=metadata
        )
        
        # Publish event to Kafka
        producer.send(TOPIC_CLICKS, {
            'id_click': click_id,
            'id_partner': request.id_partner,
            'id_campana': request.id_campana,
            'url_origen': request.url_origen,
            'url_destino': request.url_destino,
            'metadata_cliente': request.metadata_cliente,
            'timestamp': datetime.now().isoformat()
        })
        
        return click_id
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tracking/conversiones")
async def registrar_conversion(
    request: ConversionRequest,
    servicio_tracking: ServicioTracking = Depends(get_tracking_service),
    producer: KafkaProducer = Depends(get_kafka_producer)
) -> str:
    try:
        tipo = TipoConversion(request.tipo_conversion)
        info_monetaria = InformacionMonetaria(**request.informacion_monetaria)
        metadata = MetadataCliente(**request.metadata_cliente)
        
        conversion_id = servicio_tracking.registrar_conversion(
            id_partner=request.id_partner,
            id_campana=request.id_campana,
            tipo=tipo,
            informacion_monetaria=info_monetaria,
            metadata_cliente=metadata,
            id_click=request.id_click
        )
        
        producer.send(TOPIC_CONVERSIONES, {
            'id_conversion': conversion_id,
            'id_click': request.id_click,
            'id_partner': request.id_partner,
            'id_campana': request.id_campana,
            'tipo_conversion': request.tipo_conversion,
            'informacion_monetaria': request.informacion_monetaria,
            'metadata_cliente': request.metadata_cliente,
            'timestamp': datetime.now().isoformat()
        })
        
        return conversion_id
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tracking/atribuciones/{id_conversion}")
async def asignar_atribucion(
    id_conversion: str,
    request: AtribucionRequest,
    servicio_tracking: ServicioTracking = Depends(get_tracking_service),
    producer: KafkaProducer = Depends(get_kafka_producer)
):
    try:
        modelo_atribucion = ModeloAtribucion(request.modelo)
        servicio_tracking.asignar_atribucion(
            id_conversion=id_conversion,
            modelo=modelo_atribucion,
            porcentaje=request.porcentaje,
            ventana_atribucion=request.ventana_atribucion
        )
        
        # Publish event to Kafka
        producer.send(TOPIC_ATRIBUCIONES, {
            'id_conversion': id_conversion,
            'modelo': request.modelo,
            'porcentaje': request.porcentaje,
            'ventana_atribucion': request.ventana_atribucion,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tracking/conversiones/{id_partner}")
async def obtener_conversiones_partner(
    id_partner: str,
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None
) -> List[Conversion]:
    try:
        return servicio_tracking.obtener_conversiones_partner(
            id_partner=id_partner,
            desde=desde,
            hasta=hasta
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
