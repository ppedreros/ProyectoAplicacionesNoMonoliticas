from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..config.database import get_loyalty_db
from ..modulos.loyalty.aplicacion.servicios import ServicioLoyalty
from ..modulos.loyalty.dominio.objetos_valor import EstadoEmbajador
from ..modulos.loyalty.infraestructura.repositorios import RepositorioEmbajadoresSQL
from ..modulos.loyalty.infraestructura.config import get_loyalty_kafka_producer

# DTOs
class CrearEmbajadorRequest(BaseModel):
    nombre: str
    email: str
    id_partner: Optional[str] = None

class ActivarEmbajadorRequest(BaseModel):
    id_embajador: str

class RegistrarReferidoRequest(BaseModel):
    id_embajador: str
    email_referido: str
    nombre_referido: Optional[str] = None
    valor_conversion: float = 0.0
    porcentaje_comision: float = 5.0

class EmbajadorResponse(BaseModel):
    id_embajador: str
    nombre: str
    email: str
    estado: str
    id_partner: Optional[str]
    total_referidos: int
    comisiones_ganadas: float

router = APIRouter()

def get_loyalty_service(
    db: Session = Depends(get_loyalty_db)
) -> ServicioLoyalty:
    """Dependency injection para el servicio de Loyalty."""
    repositorio = RepositorioEmbajadoresSQL(db)
    despachador = get_loyalty_kafka_producer()
    return ServicioLoyalty(repositorio, despachador)

@router.post("/loyalty/embajadores", response_model=dict)
async def crear_embajador(
    request: CrearEmbajadorRequest,
    servicio: ServicioLoyalty = Depends(get_loyalty_service)
):
    """Crea un nuevo embajador en el sistema. Publica evento EmbajadorCreado en Kafka."""
    try:
        id_embajador = servicio.crear_embajador(
            nombre=request.nombre,
            email=request.email,
            id_partner=request.id_partner
        )
        
        return {
            "mensaje": "Embajador creado exitosamente",
            "id_embajador": id_embajador
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.post("/loyalty/embajadores/activar")
async def activar_embajador(
    request: ActivarEmbajadorRequest,
    servicio: ServicioLoyalty = Depends(get_loyalty_service)
):
    """Activa un embajador que estaba pendiente."""
    try:
        servicio.activar_embajador(request.id_embajador)
        
        return {
            "mensaje": "Embajador activado exitosamente",
            "id_embajador": request.id_embajador
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.post("/loyalty/referidos", response_model=dict)
async def registrar_referido(
    request: RegistrarReferidoRequest,
    servicio: ServicioLoyalty = Depends(get_loyalty_service)
):
    """Registra un nuevo referido para un embajador. Publica evento ReferidoRegistrado que será escuchado por Tracking Service."""
    try:
        id_referido = servicio.registrar_referido(
            id_embajador=request.id_embajador,
            email_referido=request.email_referido,
            nombre_referido=request.nombre_referido,
            valor_conversion=request.valor_conversion,
            porcentaje_comision=request.porcentaje_comision
        )
        
        return {
            "mensaje": "Referido registrado exitosamente",
            "id_referido": id_referido,
            "evento_publicado": "ReferidoRegistrado enviado a Kafka"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/loyalty/embajadores/{id_embajador}", response_model=EmbajadorResponse)
async def obtener_embajador(
    id_embajador: str,
    servicio: ServicioLoyalty = Depends(get_loyalty_service)
):
    """Obtiene la información de un embajador por su ID."""
    try:
        embajador = servicio.obtener_embajador_por_id(id_embajador)
        
        if not embajador:
            raise HTTPException(status_code=404, detail="Embajador no encontrado")
        
        return EmbajadorResponse(
            id_embajador=embajador.id_embajador,
            nombre=embajador.nombre,
            email=embajador.email,
            estado=embajador.estado.value,
            id_partner=embajador.id_partner,
            total_referidos=embajador.total_referidos,
            comisiones_ganadas=embajador.comisiones_ganadas
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/loyalty/partners/{id_partner}/embajadores", response_model=List[EmbajadorResponse])
async def obtener_embajadores_partner(
    id_partner: str,
    activos_solo: bool = True,
    servicio: ServicioLoyalty = Depends(get_loyalty_service)
):
    """Obtiene todos los embajadores de un partner."""
    try:
        embajadores = servicio.obtener_embajadores_partner(id_partner, activos_solo)
        
        return [
            EmbajadorResponse(
                id_embajador=emb.id_embajador,
                nombre=emb.nombre,
                email=emb.email,
                estado=emb.estado.value,
                id_partner=emb.id_partner,
                total_referidos=emb.total_referidos,
                comisiones_ganadas=emb.comisiones_ganadas
            )
            for emb in embajadores
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")