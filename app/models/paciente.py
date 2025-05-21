from typing import Optional
from sqlite3 import Row

class Paciente:
    def __init__(self, id: Optional[int] = None, nombre: str = "", edad: int = 0, peso_actual: float = 0.0):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.peso_actual = peso_actual
    
    @classmethod
    def from_row(cls, row: Row) -> "Paciente":
        return cls(
            id=row["id"],
            nombre=row["nombre"],
            edad=row["edad"],
            peso_actual=row["peso_actual"]
        )

    def __str__(self) -> str:
        return f"Paciente(id={self.id}, nombre='{self.nombre}', edad={self.edad}, peso_actual={self.peso_actual}kg)"