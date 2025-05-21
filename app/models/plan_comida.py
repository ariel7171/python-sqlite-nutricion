from typing import Optional
from sqlite3 import Row

class PlanComida:
    def __init__(self, id: Optional[int] = None, paciente_id: int = 0, alimento_id: int = 0, 
                 fecha: str = "", cantidad: float = 0.0):
        self.id = id
        self.paciente_id = paciente_id
        self.alimento_id = alimento_id
        self.fecha = fecha
        self.cantidad = cantidad
    
    @classmethod
    def from_row(cls, row: Row) -> "PlanComida":
        return cls(
            id=row["id"],
            paciente_id=row["paciente_id"],
            alimento_id=row["alimento_id"],
            fecha=row["fecha"],
            cantidad=row["cantidad"]
        )
    
    def __str__(self) -> str:
        return f"PlanComida(id={self.id}, paciente_id={self.paciente_id}, alimento_id={self.alimento_id}, fecha='{self.fecha}', cantidad={self.cantidad})"
