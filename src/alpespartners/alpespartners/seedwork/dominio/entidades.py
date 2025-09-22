"""Entidades reusables parte del seedwork del proyecto

En este archivo usted encontrará las entidades reusables parte del seedwork del proyecto

"""

from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class Entidad:
    id: str = field(default_factory=lambda: str(uuid.uuid4()), hash=True)
    fecha_creacion: datetime = field(default_factory=datetime.now)
    fecha_actualizacion: datetime = field(default_factory=datetime.now)

    @classmethod
    def siguiente_id(self) -> str:
        return str(uuid.uuid4())
        

@dataclass
class AgregacionRaiz(Entidad):
    ...


@dataclass
class Locacion(Entidad):
    def __str__(self) -> str:
        ...
