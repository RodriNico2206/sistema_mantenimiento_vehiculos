# models/servicio.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Servicio:
    id: Optional[int] = None
    vehiculo_id: int = 0
    fecha_servicio: str = ""
    tipo_servicio: str = ""
    descripcion: str = ""
    kilometraje_aplicado: int = 0
    kilometraje_proximo_servicio: int = 0
    costo: float = 0.0
    taller: str = ""
    notas: str = ""

    def __post_init__(self):
        if not self.fecha_servicio:
            self.fecha_servicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
