from datetime import datetime

def validar_fecha(fecha_str: str) -> bool:
    """Valida que una fecha tenga formato YYYY-MM-DD."""
    try:
        datetime.strptime(fecha_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def calcular_calorias_totales(cantidad: float, calorias_por_unidad: int) -> float:
    """Calcula el total de calorías basado en la cantidad y calorías unitarias."""
    return cantidad * calorias_por_unidad
