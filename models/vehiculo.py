# models/vehiculo.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Vehiculo:
    id: Optional[int] = None
    placa: str = ""
    marca: str = ""
    modelo: str = ""
    anio: Optional[int] = None
    color: str = ""
    vin: str = ""
    kilometraje_actual: int = 0
    fecha_registro: str = ""

    def __post_init__(self):
        if not self.fecha_registro:
            self.fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
