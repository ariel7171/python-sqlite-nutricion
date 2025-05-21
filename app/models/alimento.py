from typing import Optional
from sqlite3 import Row

class Alimento:
    def __init__(self, id: Optional[int] = None, nombre: str = "", calorias: int = 0):
        self.id = id
        self.nombre = nombre
        self.calorias = calorias
    
    @classmethod
    def from_row(cls, row: Row) -> "Alimento":
        return cls(
            id=row["id"],
            nombre=row["nombre"],
            calorias=row["calorias"]
        )
    
    def __str__(self) -> str:
        return f"Alimento(id={self.id}, nombre='{self.nombre}', calorias={self.calorias}kcal)"